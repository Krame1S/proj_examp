"""SQLAlchemy Attachment model — used for Alembic migration generation."""

from sqlalchemy.orm import Mapped, mapped_column
from shared.models.base import Base, TimestampMixin
import sqlalchemy as sa


class Attachment(TimestampMixin, Base):
    __tablename__ = "attachment"
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    key: Mapped[str] = mapped_column(sa.String(1024), nullable=False, unique=True)
    filename: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(sa.String(127), nullable=False)
    size: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    __table_args__ = (
        sa.Index("ix_attachment_task_id", "task_id"),
        sa.Index("ix_attachment_owner_id", "owner_id"),
        {"schema": "attachments"},
    )