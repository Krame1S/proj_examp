"""SQLAlchemy Task model — used for Alembic migration generation."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, TimestampMixin


class Task(TimestampMixin, Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey("user.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.true(), nullable=False)
