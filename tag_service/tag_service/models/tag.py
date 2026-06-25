"""SQLAlchemy Tag model — used for Alembic migration generation."""

import sqlalchemy as sa
from shared.models.base import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class Tag(TimestampMixin, Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    created_by: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    __table_args__ = (
        sa.Index("ix_tag_created_by", "created_by"),
        sa.UniqueConstraint("name", "created_by", name="uq_tag_name_created_by"),
        {"schema": "tags"},
    )
