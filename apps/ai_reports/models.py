from django.db import models

from adhocracy4.comments.models import Comment
from adhocracy4.models.base import TimeStampedModel


class AiReport(TimeStampedModel):
    is_pending = models.BooleanField(default=True)
    category = models.CharField(max_length=50)
    explanation = models.TextField()
    confidence = models.FloatField(default=0)
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="ai_report",
    )
