"""SQLAlchemy TaskTag model — used for Alembic migration generation."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class TaskTag(Base):
    __tablename__ = "task_tag"

    task_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("task.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("tag.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        sa.Index("ix_task_tag_task_id", "task_id"),
        sa.Index("ix_task_tag_tag_id", "tag_id"),
    )