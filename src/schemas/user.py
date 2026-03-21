from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: Optional[str]

    @classmethod
    def from_db_row(cls, row: dict) -> "UserProfile":
        return cls(
            id=row["id"],
            email=row["email"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"].isoformat() if row["created_at"] else None,
        )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")