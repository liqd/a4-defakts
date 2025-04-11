from django.conf import settings
from rest_framework import serializers
from wagtail.models import Site

from apps.ai_reports.models import AiReport
from apps.cms.settings.models import ImportantPages

EXCLUDED_LABELS = [
    "catneutral",
    "catnodecis",
    "catposfake",
]


class AiReportSerializer(serializers.ModelSerializer):
    explanation = serializers.SerializerMethodField()
    faq_url = serializers.SerializerMethodField()

    class Meta:
        model = AiReport
        fields = (
            "label",
            "confidence",
            "explanation",
            "is_pending",
            "comment",
            "show_in_discussion",
            "faq_url",
        )

    def to_representation(self, instance):
        if instance.label == "real" or all(
            label in EXCLUDED_LABELS for label in instance.explanation
        ):
            return None
        return super().to_representation(instance)

    def get_explanation(self, ai_report: AiReport):
        """Replace label codes with description and remove catneutral and catnodecis"""
        return [
            {
                "code": label,
                "label": settings.XAI_LABELS.get(label, label),
                "explanation": explanation,
            }
            for label, explanation in ai_report.explanation.items()
            if label not in EXCLUDED_LABELS
        ]

    def get_faq_url(self, ai_report: AiReport):
        site = Site.objects.filter(is_default_site=True).first()
        important_pages = ImportantPages.for_site(site)
        if getattr(important_pages, "faq") and getattr(important_pages, "faq").live:
            return getattr(important_pages, "faq").url
        else:
            return ""
