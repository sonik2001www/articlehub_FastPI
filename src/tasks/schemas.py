# src/tasks/schemas.py

from typing import Any, Optional

from pydantic import BaseModel


class TaskStatusOut(BaseModel):
    id: str
    state: str
    result: Optional[Any] = None
