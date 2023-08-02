from pytest_factoryboy import register

from tests.ai_reports.factories import AiReportFactory
from tests.ideas.factories import IdeaFactory

from .factories import ModeratorCommentFeedbackFactory

register(AiReportFactory)
register(IdeaFactory)
register(ModeratorCommentFeedbackFactory)
