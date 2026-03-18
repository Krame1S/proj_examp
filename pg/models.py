"""Re-export all SQLAlchemy models for Alembic auto-detection."""
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    metadata = sa.MetaData(schema=settings.DB_SCHEMA)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    passw: Mapped[str] = mapped_column(sa.String(512))
