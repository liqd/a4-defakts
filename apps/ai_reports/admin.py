from django.contrib import admin

from .models import AiReport


@admin.register(AiReport)
class AiReportAdmin(admin.ModelAdmin):
    model = AiReport
    list_display = (
        "__str__",
        "category",
        "confidence",
        "is_pending",
        "comment",
    )
    list_filter = (
        "is_pending",
        "category",
        "confidence",
        "comment",
    )
    search_fields = (
        "category",
        "explanation",
        "confidence",
        "is_pending",
    )
    fields = (
        "is_pending",
        "category",
        "explanation",
        "confidence",
        "comment",
    )
    raw_id_fields = ("comment",)
