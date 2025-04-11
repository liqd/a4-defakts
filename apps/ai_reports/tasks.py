import backoff
import httpx
from celery import shared_task
from django.conf import settings

from adhocracy4.comments.models import Comment
from apps import logger
from apps.ai_reports.models import AiReport

client = httpx.Client()


@shared_task
def get_classification_for_comment(comment_pk: int) -> None:
    try:
        comment = Comment.objects.get(pk=comment_pk)
        response = call_ai_api(comment=comment.comment)
        if response.status_code == 200:
            extract_and_save_ai_classifications(comment=comment, report=response.json())
        else:
            logger.error("Error: XAI server returned %s", response.status_code)
    except httpx.HTTPError as e:
        logger.error("Error connecting to %s: %s", settings.XAI_API_URL, str(e))


def skip_retry(e: Exception) -> bool:
    if isinstance(e, httpx.HTTPStatusError):
        return 400 <= e.response.status_code < 500
    return False


@backoff.on_exception(
    backoff.expo, httpx.HTTPError, max_tries=4, factor=2, giveup=skip_retry
)
def call_ai_api(comment: str) -> httpx.Response:
    response = client.post(
        settings.XAI_API_URL,
        json={"comment": comment},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        timeout=25.0,
    )
    response.raise_for_status()
    return response


def extract_and_save_ai_classifications(comment: Comment, report: dict) -> None:
    confidence = report["confidence"]
    label = report["label"]
    explanation = report["explanation"]

    ai_report = AiReport(
        comment=comment, confidence=confidence, label=label, explanation=explanation
    )
    ai_report.save()
