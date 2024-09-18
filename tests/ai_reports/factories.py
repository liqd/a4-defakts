import random

import factory
from django.conf import settings

from apps.ai_reports.models import AiReport
from tests.factories import CommentFactory


class AiReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AiReport

    label = factory.List(
        [
            list(settings.XAI_LABELS.keys())[
                random.randint(0, len(settings.XAI_LABELS) - 1)
            ]
            for _ in range(3)
        ]
    )
    explanation = {"xai explanation": [["first word", 0.0123]]}
    confidence = [random.random() for _ in range(3)]
    comment = factory.SubFactory(CommentFactory)
    show_in_discussion = True
