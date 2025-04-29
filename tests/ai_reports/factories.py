import random

import factory

from apps.ai_reports.models import AiReport
from tests.factories import CommentFactory


class AiReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AiReport

    label = "fake"
    explanation = {
        "catnodecis": ["word"],
        "catneutral": ["word"],
        "psychemo": ["word"],
    }
    confidence = [random.random() for _ in range(3)]
    comment = factory.SubFactory(CommentFactory)
    show_in_discussion = True
