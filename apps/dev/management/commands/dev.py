from django.core.management.base import BaseCommand

from adhocracy4.comments.models import Comment


class Command(BaseCommand):
    help = "Hannes dev command"

    def handle(self, *args, **options):
        for comment in Comment.objects.filter(ai_report__isnull=False):
            print(f"{comment=}, {comment.ai_report=}, {comment.reports=}")
