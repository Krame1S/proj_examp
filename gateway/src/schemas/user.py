from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: Optional[str]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")