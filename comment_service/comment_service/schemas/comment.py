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

    @classmethod
    def from_db_row(cls, row: dict) -> "CommentOut":
        return cls(
            id=row["id"],
            content=row["content"],
            task_id=row["task_id"],
            owner_id=row["owner_id"],
            created_at=row["created_at"].isoformat() if row.get("created_at") else None,
            updated_at=row["updated_at"].isoformat() if row.get("updated_at") else None,
        )