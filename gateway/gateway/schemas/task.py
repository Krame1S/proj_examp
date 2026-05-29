from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., max_length=4000)
    category_id: Optional[int] = Field(None, ge=1)
    tags: list[int] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.todo


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=4000)
    category_id: Optional[int] = Field(None, ge=1)
    tags: Optional[list[int]] = Field(None)
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    status: TaskStatus
    created_at: Optional[str]
    updated_at: Optional[str]


class GetTaskResponse(BaseModel):
    tasks: list[TaskOut]
    has_more: bool