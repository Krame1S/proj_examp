"""SQLAlchemy Category model — used for Alembic migration generation."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_by: Mapped[int] = mapped_column(
        sa.BigInteger,
        sa.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        sa.Index("ix_category_created_by", "created_by"),
    )