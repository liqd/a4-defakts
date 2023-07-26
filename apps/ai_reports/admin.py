from django.contrib import admin

from .models import AiReport


@admin.register(AiReport)
class AiReportAdmin(admin.ModelAdmin):
    model = AiReport
    fields = [
        "is_pending",
        "category",
        "explanation",
        "confidence",
    ]
    raw_id_fields = ("comment",)
