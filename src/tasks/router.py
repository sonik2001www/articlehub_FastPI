from fastapi import APIRouter, Depends

from src.tasks.schemas import TaskStatusOut
from src.tasks.service import TasksService
from src.tasks.dependencies import get_tasks_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskStatusOut)
def task_status(
    task_id: str,
    svc: TasksService = Depends(get_tasks_service),
):
    """
    Returns the status of a Celery task by task_id.
    """
    data = svc.get_status(task_id)
    return TaskStatusOut(**data)
