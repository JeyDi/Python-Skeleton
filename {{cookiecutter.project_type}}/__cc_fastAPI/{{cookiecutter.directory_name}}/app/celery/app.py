from celery import Celery

from app.src.config import settings

worker = Celery(
    "fastapi_celery_app",
    broker=settings.CELERY_BROKER_URI,
    backend=settings.CELERY_BACKEND_URI,
    include=["app.celery.task.worker"],
)
