from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from apps.ai_reports.models import AiReport
from apps.contrib import dates


@pytest.mark.django_db
def test_num_reports(
    apiclient,
    report_factory,
    ai_report_factory,
    comment_factory,
    idea,
):
    comments = comment_factory.create_batch(size=4, content_object=idea)
    comments = {comment.pk: comment for comment in comments}
    pks = list(comments)

    n_user_reports = [1, 3, 0, 0]
    num_user_reports_created = dict(zip(pks, n_user_reports))
    for pk, size in num_user_reports_created.items():
        report_factory.create_batch(size=size, content_object=comments[pk])

    has_ai_report = [True, False, True, False]
    ai_reports_created = dict(zip(comments, has_ai_report))
    for pk, has_ai_report in ai_reports_created.items():
        if has_ai_report:
            ai_report_factory(comment=comments[pk])

    num_reports_created = {
        i: num_user_reports_created[i] + int(ai_reports_created[i]) for i in pks
    }

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)

    assert response.status_code == 200
    assert len(response.data) == 4

    num_reports_received = {
        comment["pk"]: comment["num_reports"] for comment in response.data
    }

    ai_reports_received = {
        comment["pk"]: True if comment["ai_report"] else False
        for comment in response.data
    }
    ai_report_objects = AiReport.objects.prefetch_related("comment")

    assert num_reports_created == num_reports_received
    assert ai_reports_created == ai_reports_received
    for ai in ai_report_objects:
        for comment in response.data:
            if (
                comment["ai_report"]
                and comment["ai_report"]["comment"] == ai.comment.pk
            ):
                assert comment["ai_report"]["label"] == [
                    (label, settings.XAI_LABELS[label]) for label in ai.label
                ]
                assert comment["ai_report"]["explanation"] == ai.explanation
                assert comment["ai_report"]["confidence"] == ai.confidence
                assert comment["ai_report"]["is_pending"] == ai.is_pending
                assert comment["ai_report"]["faq_url"] == ""


@pytest.mark.django_db
def test_last_edit(apiclient, report_factory, comment_factory, idea):
    comment_1 = comment_factory(content_object=idea)
    report_factory(content_object=comment_1)
    comment_2 = comment_factory(content_object=idea)
    report_factory(content_object=comment_2)

    with freeze_time(comment_2.created + timedelta(minutes=3)):
        comment_2.modified = timezone.now()
        comment_2.save()

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    comment_1_data = [
        comment for comment in response.data if comment["pk"] == comment_1.pk
    ][0]
    comment_2_data = [
        comment for comment in response.data if comment["pk"] == comment_2.pk
    ][0]

    assert not comment_1_data["is_modified"]
    assert comment_1_data["last_edit"] == dates.get_date_display(comment_1.created)
    assert comment_2_data["is_modified"]
    assert comment_2_data["last_edit"] == dates.get_date_display(comment_2.modified)


@pytest.mark.django_db
def test_fields(
    apiclient, report_factory, comment_factory, idea, moderator_comment_feedback_factory
):
    comments_created = [
        comment_factory(content_object=idea, is_moderator_marked=True),
        comment_factory(content_object=idea, is_blocked=True),
        comment_factory(content_object=idea, is_removed=True),
    ]

    report_factory(content_object=comments_created[0])
    report_factory.create_batch(size=2, content_object=comments_created[1])
    feedback = moderator_comment_feedback_factory(comment=comments_created[2])

    with freeze_time(comments_created[1].created + timedelta(minutes=3)):
        comments_created[1].modified = timezone.now()
        comments_created[1].save()

    project = idea.project
    moderator = project.moderators.first()
    apiclient.login(username=moderator.email, password="password")
    url = reverse("moderationcomments-list", kwargs={"project_pk": project.pk})
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    comments_received = []
    for comment in comments_created:
        for comment_data in response.data:
            if comment_data["pk"] == comment.pk:
                comments_received.append(comment_data)
                break

    for data, comment in zip(comments_received, comments_created):
        assert len(data["user_reports"]) == comment.reports.count()

    assert comments_received[0]["comment"] == comments_created[0].comment
    assert comments_received[0]["comment_url"] == comments_created[0].get_absolute_url()
    assert comments_received[0]["is_unread"]
    assert not comments_received[0]["is_blocked"]
    assert comments_received[0]["is_moderator_marked"]
    assert not comments_received[0]["is_modified"]
    assert comments_received[0]["last_edit"] == dates.get_date_display(
        comments_created[0].created
    )
    assert comments_received[0]["moderator_feedback"] is None
    assert comments_received[0]["num_reports"] == 1
    assert comments_received[0]["pk"] == comments_created[0].pk
    assert comments_received[0]["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comments_created[0].pk}
    )
    assert (
        comments_received[0]["user_image"]
        == comments_created[0].creator.avatar_fallback
    )
    assert comments_received[0]["user_name"] == comments_created[0].creator.username
    assert (
        comments_received[0]["user_profile_url"]
        == comments_created[0].creator.get_absolute_url()
    )

    assert comments_received[1]["comment"] == comments_created[1].comment
    assert comments_received[1]["comment_url"] == comments_created[1].get_absolute_url()
    assert comments_received[1]["is_unread"]
    assert comments_received[1]["is_blocked"]
    assert not comments_received[1]["is_moderator_marked"]
    assert comments_received[1]["is_modified"]
    assert comments_received[1]["last_edit"] == dates.get_date_display(
        comments_created[1].modified
    )
    assert comments_received[1]["moderator_feedback"] is None
    assert comments_received[1]["num_reports"] == 2
    assert comments_received[1]["pk"] == comments_created[1].pk
    assert comments_received[1]["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comments_created[1].pk}
    )
    assert (
        comments_received[1]["user_image"]
        == comments_created[1].creator.avatar_fallback
    )
    assert comments_received[1]["user_name"] == comments_created[1].creator.username
    assert (
        comments_received[1]["user_profile_url"]
        == comments_created[1].creator.get_absolute_url()
    )

    assert comments_received[2]["comment"] == comments_created[2].comment == ""
    assert comments_received[2]["comment_url"] == comments_created[2].get_absolute_url()
    assert comments_received[2]["is_unread"]
    assert not comments_received[2]["is_blocked"]
    assert not comments_received[2]["is_moderator_marked"]
    assert not comments_received[2]["is_modified"]
    assert comments_received[2]["last_edit"] == dates.get_date_display(
        comments_created[2].created
    )
    assert comments_received[2]["moderator_feedback"] is not None
    assert (
        comments_received[2]["moderator_feedback"]["feedback_text"]
        == feedback.feedback_text
    )
    assert comments_received[2]["num_reports"] == 0
    assert comments_received[2]["pk"] == comments_created[2].pk
    assert comments_received[2]["feedback_api_url"] == reverse(
        "moderatorfeedback-list", kwargs={"comment_pk": comments_created[2].pk}
    )
    assert comments_received[2]["user_image"] is None
    assert comments_received[2]["user_name"] == "unknown user"
    assert comments_received[2]["user_profile_url"] == ""
