from typing import Optional

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class TagOut(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_db_row(cls, row: dict) -> "TagOut":
        return cls(
            id=row["id"],
            name=row["name"],
            created_by=row["created_by"],
            created_at=row["created_at"].isoformat() if row.get("created_at") else None,
            updated_at=row["updated_at"].isoformat() if row.get("updated_at") else None,
        )