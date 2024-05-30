from pytest_factoryboy import register

from tests.ideas import factories as idea_factories

from .factories import AiReportFactory

register(AiReportFactory)
register(idea_factories.IdeaFactory)
