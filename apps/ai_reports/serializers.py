from django.conf import settings
from rest_framework import serializers
from wagtail.models import Site

from apps.ai_reports.models import AiReport
from apps.cms.settings.models import ImportantPages


class AiReportSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
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

    def get_label(self, ai_report: AiReport):
        """Replace label codes with description and remove catneutral and catnodecis"""
        return [
            (label, settings.XAI_LABELS.get(label, label))
            for label in ai_report.label
            if label != "catneutral" and label != "catnodecis"
        ]

    def get_faq_url(self, ai_report: AiReport):
        site = Site.objects.filter(is_default_site=True).first()
        important_pages = ImportantPages.for_site(site)
        if getattr(important_pages, "faq") and getattr(important_pages, "faq").live:
            return getattr(important_pages, "faq").url
        else:
            return ""
