from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "articlehub",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_RESULT_BACKEND,
    include=["app.workers.tasks"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.task_routes = {
    "app.workers.tasks.send_welcome_email": {"queue": "emails"},
    "app.workers.tasks.daily_articles_stats": {"queue": "stats"},
    "app.workers.tasks.analyze_article": {"queue": "analysis"},
}

# Celery beat schedule (02:00 UTC)
celery_app.conf.beat_schedule = {
    "daily-articles-stats": {
        "task": "app.workers.tasks.daily_articles_stats",
        "schedule": 24 * 60 * 60,
        "options": {"queue": "stats"},
    }
}