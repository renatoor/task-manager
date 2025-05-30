from celery import Celery

from app.core.config import CELERY_BACKEND_URL, CELERY_BROKER_URL

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
)

celery_app.conf.task_routes = {
    "app.infrastructure.worker_tasks.*": {"queue": "default"}
}
