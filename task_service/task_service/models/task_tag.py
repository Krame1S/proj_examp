"""SQLAlchemy TaskTag model — used for Alembic migration generation."""

import sqlalchemy as sa
from shared.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class TaskTag(Base):
    __tablename__ = "task_tag"
    task_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    tag_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    __table_args__ = (
        sa.Index("ix_task_tag_task_id", "task_id"),
        sa.Index("ix_task_tag_tag_id", "tag_id"),
        {"schema": "tasks"},
    )
