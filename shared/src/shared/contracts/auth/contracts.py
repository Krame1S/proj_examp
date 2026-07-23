from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class SignUpRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(...)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class SignInRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: Optional[str] = None

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
