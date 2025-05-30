from app.core.worker import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task
def send_email(email: str, content: str):
    logger.info(f"Sending email to {email}, content: {content}")
