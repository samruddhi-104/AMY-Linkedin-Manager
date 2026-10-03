from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    command: str = Field(min_length=1, max_length=5000)
    task_type: str = "GENERAL"
    priority: str = "normal"
    company_id: UUID | None = None
    created_by: UUID | None = None


class TaskUpdate(BaseModel):
    status: str | None = None
    progress: int | None = Field(default=None, ge=0, le=100)
    result: dict[str, Any] | None = None
    error: str | None = None


class TaskResponse(BaseModel):
    id: UUID
    task_type: str
    status: str
    command: str
    progress: int
    priority: str
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }