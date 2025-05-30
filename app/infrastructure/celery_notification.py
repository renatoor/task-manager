from loguru import logger

from app.infrastructure.worker_tasks.send_email import send_email


class CeleryNotification:
    def send_email(self, email: str, content: str):
        logger.info("Sending email notification")
        result = send_email.delay(email, content)
        logger.info(f"Result - id: {result.id}, status: {result.status}")
