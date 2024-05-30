import pytest
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from adhocracy4.comments.models import Comment
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from apps.ai_reports.signals import get_ai_classification
from apps.ideas.models import Idea
from apps.ideas.phases import CollectPhase
from apps.ideas.phases import RatingPhase


@pytest.mark.django_db
def test_comment_not_sent_to_xai_no_url(mocker, idea, comment_factory, caplog):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment" ".delay"
    )
    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    comment_factory(content_object=idea, comment="lala")
    task_mock.assert_not_called()


@override_settings(XAI_API_URL="https://liqd.net")
@pytest.mark.django_db
def test_comment_sent_to_xai_on_comment_text_change(mocker, idea, comment_factory):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment" ".delay"
    )

    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    comment = comment_factory(content_object=idea, comment="lala")
    task_mock.assert_called_once_with(comment.pk)
    task_mock.reset_mock()

    comment.comment = "modified comment"
    comment.save()
    task_mock.assert_called_once_with(comment.pk)


@override_settings(XAI_API_URL="https://liqd.net")
@pytest.mark.django_db
def test_comment_not_sent_to_xai_without_comment_text_change(
    mocker, idea, comment_factory, caplog
):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment" ".delay"
    )
    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    comment = comment_factory(content_object=idea, comment="lala")
    task_mock.assert_called_once_with(comment.pk)
    task_mock.reset_mock()

    comment.is_blocked = True
    comment.save()
    task_mock.assert_not_called()


@override_settings(XAI_API_URL="https://liqd.net")
@pytest.mark.django_db
def test_comment_posted_via_api_sent_to_xai(
    mocker, apiclient, idea_factory, organisation_terms_of_use_factory, phase_factory
):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment.delay"
    )
    phase, _, project, idea = setup_phase(phase_factory, idea_factory, RatingPhase)
    _, moderator, _ = setup_users(project)
    organisation_terms_of_use_factory(
        user=moderator,
        organisation=project.organisation,
        has_agreed=True,
    )
    apiclient.force_authenticate(user=moderator)
    content_type = ContentType.objects.get_for_model(Idea)

    url = reverse(
        "comments-list",
        kwargs={"content_type": content_type.pk, "object_pk": idea.pk},
    )
    data = {"comment": "comment comment"}

    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    with freeze_phase(phase):
        response = apiclient.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1
        task_mock.assert_called_once_with(Comment.objects.first().pk)


@override_settings(XAI_API_URL="https://liqd.net")
@pytest.mark.django_db
def test_comment_edited_via_api_sent_to_xai(
    mocker,
    apiclient,
    comment_factory,
    idea_factory,
    organisation_terms_of_use_factory,
    phase_factory,
):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment.delay"
    )
    phase, _, _, idea = setup_phase(phase_factory, idea_factory, CollectPhase)
    comment = comment_factory(content_object=idea)
    task_mock.assert_called_once_with(comment.pk)
    task_mock.reset_mock()

    organisation_terms_of_use_factory(
        user=comment.creator,
        organisation=comment.project.organisation,
        has_agreed=True,
    )
    apiclient.force_authenticate(user=comment.creator)

    url = reverse(
        "comments-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"comment": "comment new comment"}

    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    with freeze_phase(phase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        task_mock.assert_called_once_with(comment.pk)


@override_settings(XAI_API_URL="https://liqd.net")
@pytest.mark.django_db
def test_comment_edited_not_text_via_api_not_sent_to_xai(
    mocker,
    apiclient,
    comment_factory,
    idea_factory,
    organisation_terms_of_use_factory,
    phase_factory,
):
    task_mock = mocker.patch(
        "apps.ai_reports.tasks.get_classification_for_comment.delay"
    )
    phase, _, _, idea = setup_phase(phase_factory, idea_factory, CollectPhase)
    comment = comment_factory(content_object=idea)
    task_mock.assert_called_once_with(comment.pk)
    task_mock.reset_mock()

    organisation_terms_of_use_factory(
        user=comment.creator,
        organisation=comment.project.organisation,
        has_agreed=True,
    )
    apiclient.force_authenticate(user=comment.creator)

    url = reverse(
        "comments-detail",
        kwargs={
            "pk": comment.pk,
            "content_type": comment.content_type.pk,
            "object_pk": comment.object_pk,
        },
    )
    data = {"is_removed": True}

    assert get_ai_classification in signals.post_save._live_receivers(Comment)
    with freeze_phase(phase):
        response = apiclient.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_removed"] is True
        task_mock.assert_not_called()
