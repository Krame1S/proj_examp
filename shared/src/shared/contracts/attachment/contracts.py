from typing import Optional

from pydantic import BaseModel


class AttachmentCreateRequest(BaseModel):
    task_id: int
    owner_id: int
    key: str
    filename: str
    content_type: str
    size: int


class AttachmentOut(BaseModel):
    id: int
    task_id: int
    owner_id: int
    filename: str
    content_type: str
    size: int
    url: str
    created_at: Optional[str] = None
