from enum import Enum
from typing import Any

from pydantic import BaseModel


class ChatRequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELLED = "cancelled"


class ChatRequestIn(BaseModel):
    email: str


class ChatRequestOut(BaseModel):
    id: int
    status: ChatRequestStatus
    requester_id: int
    target_id: int
    created_at: str | None
    updated_at: str | None

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "ChatRequestOut":
        return cls(
            id=row["id"],
            status=row["status"],
            requester_id=row["requester_id"],
            target_id=row["target_id"],
            created_at=row["created_at"].isoformat() if row.get("created_at") else None,
            updated_at=row["updated_at"].isoformat() if row.get("updated_at") else None,
        )


class MessageIn(BaseModel):
    content: str


class MessageOut(BaseModel):
    id: int
    room_id: int
    sender_id: int
    content: str
    created_at: str | None

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "MessageOut":
        return cls(
            id=row["id"],
            room_id=row["room_id"],
            sender_id=row["sender_id"],
            content=row["content"],
            created_at=row["created_at"].isoformat() if row.get("created_at") else None,
        )


class GetMessagesResponse(BaseModel):
    messages: list[MessageOut]
    has_more: bool
