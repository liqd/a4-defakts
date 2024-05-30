from django.db import models

from adhocracy4.comments.models import Comment
from adhocracy4.models.base import TimeStampedModel


class AiReport(TimeStampedModel):
    is_pending = models.BooleanField(default=True)
    label = models.JSONField()
    explanation = models.JSONField()
    confidence = models.JSONField()
    show_in_discussion = models.BooleanField(default=True)
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="ai_report",
    )

    def __str__(self):
        return "%s" % (self.explanation)
