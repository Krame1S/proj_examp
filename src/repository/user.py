from typing import Any, Dict, Optional
from src.repository.base import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, email: str, password_hash: str) -> Dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO "user" (email, password_hash)
            VALUES ($1, $2)
            RETURNING id, email, is_active, created_at
            """,
            email,
            password_hash,
        )
        if record is None:
            raise RuntimeError("User creation failed - no row returned")
        return dict(record)

    async def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id, email, is_active, created_at
            FROM "user"
            WHERE id = $1
            """,
            user_id,
        )
        return dict(record) if record is not None else None

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id, email, password_hash, is_active, created_at
            FROM "user"
            WHERE email = $1
            """,
            email,
        )
        return dict(record) if record is not None else None

    async def update_email(self, user_id: int, email: str) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            UPDATE "user"
            SET email = $2, updated_at = NOW()
            WHERE id = $1
            RETURNING id, email, is_active, created_at
            """,
            user_id,
            email,
        )
        return dict(record) if record is not None else None

    async def delete(self, user_id: int) -> bool:
        result = await self.execute(
            """
            DELETE FROM "user"
            WHERE id = $1
            """,
            user_id,
        )
        return result == "DELETE 1"
