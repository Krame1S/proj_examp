"""SQLAlchemy Tag model — used for Alembic migration generation."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, TimestampMixin


class Tag(TimestampMixin, Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False, unique=True, index=True)
    created_by: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tasks: Mapped[list["Task"]] = relationship(  # type: ignore
        "Task",
        secondary="task_tag",
        back_populates="tags",
        lazy="selectin",
    )

    __table_args__ = (
        sa.Index("ix_tag_created_by", "created_by"),
    )