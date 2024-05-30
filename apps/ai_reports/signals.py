import httpx
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.comments.models import Comment
from apps.ai_reports.tasks import get_classification_for_comment

client = httpx.Client()


@receiver(signals.post_save, sender=Comment)
def get_ai_classification(sender, instance, created, update_fields, **kwargs):
    if getattr(settings, "XAI_API_URL"):
        comment_text_changed = getattr(instance, "_former_comment") != getattr(
            instance, "comment"
        )
        if created or comment_text_changed:
            # FIXME: use delay_on_commit() once updated to celery 5.x
            get_classification_for_comment.delay(instance.pk)
