from src.tasks.service import TasksService
from src.tasks.celery_app import celery_app


def get_tasks_service() -> TasksService:
    return TasksService(celery_app)
