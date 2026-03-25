from typing import Any, Dict, List, Optional
from src.repository.base import BaseRepository


class CategoryRepository(BaseRepository):

    async def create(
        self,
        name: str,
        description: str | None,
        created_by: int,
    ) -> Dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO category (name, description, created_by)
            VALUES ($1, $2, $3)
            RETURNING id, name, description, created_by, created_at, updated_at
            """,
            name,
            description,
            created_by,
        )
        if record is None:
            raise RuntimeError("Category creation failed - no row returned")
        return dict(record)

    async def get_by_id(self, category_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает категорию ТОЛЬКО если она принадлежит пользователю"""
        record = await self.fetch_row(
            """
            SELECT id, name, description, created_by, created_at, updated_at
            FROM category
            WHERE id = $1 AND created_by = $2
            """,
            category_id,
            user_id,
        )
        return dict(record) if record is not None else None

    async def get_by_name(self, name: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Проверяет существование категории с таким именем у конкретного пользователя"""
        record = await self.fetch_row(
            """
            SELECT id, name, description, created_by, created_at, updated_at
            FROM category
            WHERE name = $1 AND created_by = $2
            """,
            name,
            user_id,
        )
        return dict(record) if record is not None else None

    async def list_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, name, description, created_by, created_at, updated_at
            FROM category
            WHERE created_by = $1
            ORDER BY name ASC
            """,
            user_id,
        )
        return [dict(r) for r in records]

    async def update(
        self,
        category_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            UPDATE category
            SET 
                name = COALESCE($2, name),
                description = COALESCE($3, description),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, name, description, created_by, created_at, updated_at
            """,
            category_id,
            name,
            description,
        )
        return dict(record) if record is not None else None

    async def delete(self, category_id: int) -> bool:
        result = await self.execute(
            """
            DELETE FROM category
            WHERE id = $1
            """,
            category_id,
        )
        return result == "DELETE 1"