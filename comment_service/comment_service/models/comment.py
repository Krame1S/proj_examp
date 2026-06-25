"""SQLAlchemy Comment model — used for Alembic migration generation."""

from shared.models.base import Base, TimestampMixin
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

class Comment(TimestampMixin, Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    task_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    __table_args__ = (
        sa.Index("ix_comment_task_id", "task_id"),
        sa.Index("ix_comment_owner_id", "owner_id"),
        {"schema": "comments"},
    )