from django.apps import AppConfig


class AiReportsConfig(AppConfig):
    name = "apps.ai_reports"

    def ready(self):
        import apps.ai_reports.signals  # noqa:F401
