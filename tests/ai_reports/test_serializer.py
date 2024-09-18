import pytest
from django.conf import settings

from apps.ai_reports.serializers import AiReportSerializer


@pytest.mark.django_db
def test_serializer_filters_neutral_labels(
    apiclient,
    comment_factory,
    idea_factory,
    module_factory,
    project_factory,
    ai_report_factory,
):
    project = project_factory()
    module = module_factory(project=project)
    idea = idea_factory(module=module)
    comment = comment_factory(content_object=idea)
    ai_report = ai_report_factory(
        label=["catnodecis", "catneutral", "psychemo"], comment=comment
    )
    serializer = AiReportSerializer(ai_report)
    result = serializer.data
    assert len(result["label"]) == 1
    assert result["label"] == [("psychemo", settings.XAI_LABELS["psychemo"])]
    assert result["faq_url"] == ""
