"""SQLAlchemy Chat models — used for Alembic migration generation."""

import sqlalchemy as sa
from shared.models.base import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class ChatRequest(TimestampMixin, Base):
    __tablename__ = "chat_request"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    requester_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    target_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(sa.String(20), nullable=False, server_default="pending")

    __table_args__ = ({"schema": "chats"},)


class ChatMessage(Base):
    __tablename__ = "chat_message"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    sender_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    created_at: Mapped[sa.DateTime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    __table_args__ = (
        sa.Index("ix_chat_message_room_id_id", "room_id", "id"),
        {"schema": "chats"},
    )
