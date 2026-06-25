"""SQLAlchemy Task model — used for Alembic migration generation."""

import enum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.models.base import Base, TimestampMixin


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


task_status_enum = sa.Enum(TaskStatus, name="taskstatus")


class Task(TimestampMixin, Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(task_status_enum, nullable=False, server_default="todo")
    category_id: Mapped[int | None] = mapped_column(sa.BigInteger, nullable=True)
    __table_args__ = (
        sa.Index("ix_task_owner_id", "owner_id"),
        sa.Index("ix_task_category_id", "category_id"),
        {"schema": "tasks"},
    )