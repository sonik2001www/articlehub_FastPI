from celery import Celery

from src.config import settings


celery_app = Celery(
    "articlehub",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_RESULT_BACKEND,
    include=["src.tasks.worker"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.task_routes = {
    "src.tasks.worker.send_welcome_email": {"queue": "emails"},
    "src.tasks.worker.daily_articles_stats": {"queue": "stats"},
    "src.tasks.worker.analyze_article": {"queue": "analysis"},
}

celery_app.conf.beat_schedule = {
    "daily-articles-stats": {
        "task": "src.tasks.worker.daily_articles_stats",
        "schedule": 24 * 60 * 60,
        "options": {"queue": "stats"},
    }
}
