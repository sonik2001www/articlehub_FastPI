from celery.result import AsyncResult

from src.tasks.celery_app import celery_app


class TasksService:
    def __init__(self, app=celery_app):
        self.app = app

    def get_status(self, task_id: str) -> dict:
        r = AsyncResult(task_id, app=self.app)
        return {
            "id": task_id,
            "state": r.state,
            "result": r.result if r.successful() else None,
        }
