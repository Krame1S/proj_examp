from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int
    task_count: int = 0
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_db_row(cls, row: dict) -> "CategoryOut":
        return cls(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_by=row["created_by"],
            task_count=row.get("task_count", 0),
            created_at=row["created_at"].isoformat() if row["created_at"] else None,
            updated_at=row["updated_at"].isoformat() if row["updated_at"] else None,
        )