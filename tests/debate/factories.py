import factory

from adhocracy4.test import factories as a4_factories
from apps.debate import models


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subject

    creator = factory.SubFactory(a4_factories.USER_FACTORY)
    module = factory.SubFactory(a4_factories.ModuleFactory)
