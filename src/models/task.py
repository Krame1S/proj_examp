"""SQLAlchemy Task model — used for Alembic migration generation."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, TimestampMixin


class Task(TimestampMixin, Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true(), nullable=False)
    category_id: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    tags: Mapped[list["Tag"]] = relationship(  # type: ignore
        "Tag",
        secondary="task_tag",
        back_populates="tasks",
        lazy="selectin",
    )

    __table_args__ = (
        sa.Index("ix_task_owner_id", "owner_id"),
        sa.Index("ix_task_category_id", "category_id"),
    )