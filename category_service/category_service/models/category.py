"""SQLAlchemy Category model — used for Alembic migration generation."""

import sqlalchemy as sa
from shared.models.base import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class Category(TimestampMixin, Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_by: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    __table_args__ = (
        sa.Index("ix_category_created_by", "created_by"),
        {"schema": "categories"},
    )
