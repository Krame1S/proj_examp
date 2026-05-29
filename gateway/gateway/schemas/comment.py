from typing import Optional
from pydantic import BaseModel, Field


class CommentIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class CommentOut(BaseModel):
    id: int
    content: str
    task_id: int
    owner_id: int
    created_at: Optional[str]
    updated_at: Optional[str]