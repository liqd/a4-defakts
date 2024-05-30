from django.contrib import admin

from .models import AiReport


@admin.register(AiReport)
class AiReportAdmin(admin.ModelAdmin):
    model = AiReport
    list_display = (
        "__str__",
        "label",
        "confidence",
        "is_pending",
        "comment",
    )
    list_filter = (
        "is_pending",
        "label",
        "confidence",
        "comment",
    )
    search_fields = (
        "label",
        "explanation",
        "confidence",
        "is_pending",
    )
    fields = (
        "is_pending",
        "label",
        "explanation",
        "confidence",
        "comment",
    )
    raw_id_fields = ("comment",)
