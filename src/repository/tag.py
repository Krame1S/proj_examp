from typing import Any, Dict, List, Optional

import asyncpg

from src.repository.base import BaseRepository


class TagRepository(BaseRepository):

    async def create(
        self,
        name: str,
        created_by: int,
    ) -> Dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO tag (name, created_by)
            VALUES ($1, $2)
            RETURNING id, name, created_by, created_at, updated_at
            """,
            name,
            created_by,
        )
        if record is None:
            raise RuntimeError("Tag creation failed - no row returned")
        return dict(record)

    async def get_by_id(self, tag_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id, name, created_by, created_at, updated_at
            FROM tag
            WHERE id = $1 AND created_by = $2
            """,
            tag_id,
            user_id,
        )
        return dict(record) if record is not None else None

    async def get_by_name(self, name: str, user_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id, name, created_by, created_at, updated_at
            FROM tag
            WHERE name = $1 AND created_by = $2
            """,
            name,
            user_id,
        )
        return dict(record) if record is not None else None

    async def list_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, name, created_by, created_at, updated_at
            FROM tag
            WHERE created_by = $1
            ORDER BY name ASC
            """,
            user_id,
        )
        return [dict(r) for r in records]

    async def update(
        self,
        tag_id: int,
        name: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            UPDATE tag
            SET 
                name = COALESCE($2, name),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, name, created_by, created_at, updated_at
            """,
            tag_id,
            name,
        )
        return dict(record) if record is not None else None

    async def delete(self, tag_id: int) -> bool:
        result = await self.execute(
            """
            DELETE FROM tag
            WHERE id = $1
            """,
            tag_id,
        )
        return result == "DELETE 1"