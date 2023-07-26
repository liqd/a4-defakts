from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import BooleanFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.filters.rest_filters import DefaultsRestFilterSet
from adhocracy4.filters.rest_filters import DistinctOrderingFilter
from adhocracy4.projects.models import Project
from apps.notifications.emails import NotifyCreatorOnModeratorBlocked
from apps.projects import helpers

from . import serializers


class ModerationCommentFilterSet(DefaultsRestFilterSet):
    is_reviewed = BooleanFilter()

    defaults = {"is_reviewed": "false"}

    @property
    def qs(self):
        queryset = super().qs
        reported_by = self.request.query_params.get("reported_by")

        if reported_by == "ai":
            queryset = queryset.filter(ai_report__isnull=False)
        elif reported_by == "users":
            queryset = queryset.filter(reports__isnull=False)

        return queryset


class ModerationCommentPagination(PageNumberPagination):
    page_size_query_param = "num_of_comments"
    max_page_size = 1000


class ModerationCommentViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.ModerationCommentSerializer
    pagination_class = ModerationCommentPagination
    permission_classes = (ViewSetRulesPermission,)
    filter_backends = (DjangoFilterBackend, DistinctOrderingFilter)
    filterset_class = ModerationCommentFilterSet
    ordering_fields = ["created", "num_reports"]
    ordering = ["-num_reports"]
    # sets the attr for the distinct ordering in DistinctOrderingFilter
    distinct_ordering = "-created"
    lookup_field = "pk"

    def dispatch(self, request, *args, **kwargs):
        self.project_pk = kwargs.get("project_pk", "")
        return super().dispatch(request, *args, **kwargs)

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.project_pk)

    def get_permission_object(self):
        return self.project

    def get_queryset(self):
        comments = helpers.get_all_comments_project(self.project)
        comments = comments.annotate(
            num_reports=Count("reports", distinct=True)
            + Count("ai_report", distinct=True),
        )

        return comments

    def update(self, request, *args, **kwargs):
        if request.data.get("is_blocked"):
            NotifyCreatorOnModeratorBlocked.send(self.get_object())

        return super().update(request, *args, **kwargs)

    @action(detail=True)
    def mark_read(self, request, **kwargs):
        comment = self.get_object()
        comment.is_reviewed = True
        comment.save(ignore_modified=True)
        serializer = self.get_serializer(comment)

        return Response(data=serializer.data, status=200)

    @action(detail=True)
    def mark_unread(self, request, **kwargs):
        comment = self.get_object()
        comment.is_reviewed = False
        comment.save(ignore_modified=True)
        serializer = self.get_serializer(comment)

        return Response(data=serializer.data, status=200)

    @property
    def rules_method_map(self):
        return ViewSetRulesPermission.default_rules_method_map._replace(
            GET="a4_candy_userdashboard.view_moderation_comment",
            PUT="a4_candy_userdashboard.change_moderation_comment",
            PATCH="a4_candy_userdashboard.change_moderation_comment",
            OPTIONS="a4_candy_userdashboard.view_moderation_comment",
        )
