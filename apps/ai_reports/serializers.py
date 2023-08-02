from rest_framework import serializers

from apps.ai_reports.models import AiReport


class AiReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiReport
        fields = (
            "explanation",
            "category",
            "comment",
        )
