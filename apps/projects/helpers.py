from datetime import timedelta

from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone

from adhocracy4.comments.models import Comment


def get_all_comments_project(project):
    return Comment.objects.filter(
        Q(project=project) | Q(parent_comment__project=project)
    )


def get_num_comments_project(project):
    return get_all_comments_project(project).count()


def get_num_reports(project):
    comments = get_all_comments_project(project)
    comments = comments.annotate(
        num_reports=Count("reports", distinct=True) + Count("ai_report", distinct=True),
    )

    return comments.aggregate(Sum("num_reports"))["num_reports__sum"]


def get_num_latest_comments(project, until={"days": 7}):
    all_comments_project = get_all_comments_project(project)
    return all_comments_project.filter(
        created__gte=timezone.now() - timedelta(**until)
    ).count()


def get_num_reported_unread_comments(project):
    unread_comments = get_all_comments_project(project).filter(is_reviewed=False)
    return (
        unread_comments.annotate(num_reports=Count("reports", distinct=True))
        .filter(num_reports__gt=0)
        .count()
    )
