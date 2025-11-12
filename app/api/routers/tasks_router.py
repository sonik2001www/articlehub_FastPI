# app/api/routers/tasks_router.py (опційно)
from fastapi import APIRouter
from celery.result import AsyncResult
from app.workers.celery_app import celery_app

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/{task_id}")
def task_status(task_id: str):
    r = AsyncResult(task_id, app=celery_app)
    return {"id": task_id, "state": r.state, "result": r.result if r.successful() else None}
