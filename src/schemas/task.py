from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., max_length=4000)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=4000)
    is_active: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_db_row(cls, row: dict) -> "TaskOut":
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            owner_id=row["owner_id"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"].isoformat() if row["created_at"] else None,
            updated_at=row["updated_at"].isoformat() if row["updated_at"] else None,
        )