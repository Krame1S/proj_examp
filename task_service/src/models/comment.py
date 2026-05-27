import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base, TimestampMixin


class Comment(TimestampMixin, Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    task_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey("task.id", ondelete="CASCADE"), nullable=False
    )
    owner_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)

    __table_args__ = (
        sa.Index("ix_comment_task_id", "task_id"),
        sa.Index("ix_comment_owner_id", "owner_id"),
    )