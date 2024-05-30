import json

from rest_framework import serializers

from apps.ai_reports.models import AiReport


class AiReportSerializer(serializers.ModelSerializer):
    explanation = serializers.SerializerMethodField()

    class Meta:
        model = AiReport
        fields = (
            "label",
            "confidence",
            "explanation",
            "is_pending",
            "comment",
            "show_in_discussion",
        )

    # FIXME: remove once frontend knows what to do with this
    def get_explanation(self, ai_report: AiReport) -> str:
        return json.dumps(ai_report.explanation)
