import random

import factory

from apps.ai_reports.models import AiReport
from tests.factories import CommentFactory


class AiReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AiReport

    category = factory.Faker("word")
    explanation = factory.Faker("sentence", nb_words=6)
    confidence = random.random()
    comment = factory.SubFactory(CommentFactory)
