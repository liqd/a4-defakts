from pytest_factoryboy import register

from tests.ai_reports.factories import AiReportFactory
from tests.ideas.factories import IdeaFactory
from tests.moderatorfeedback.factories import ModeratorCommentFeedbackFactory

register(IdeaFactory)
register(ModeratorCommentFeedbackFactory)
register(AiReportFactory)
