from typing import Any

from shared.repository.base import BaseRepository


class CategoryRepository(BaseRepository):
    async def create(
        self,
        name: str,
        description: str | None,
        created_by: int,
    ) -> dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO categories.category (name, description, created_by)
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

    async def get_by_id(self, category_id: int, user_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT id, name, description, created_by, created_at, updated_at
            FROM categories.category
            WHERE id = $1 AND created_by = $2
            """,
            category_id,
            user_id,
        )
        return dict(record) if record is not None else None

    async def get_by_name(self, name: str, user_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT id, name, description, created_by, created_at, updated_at
            FROM categories.category
            WHERE name = $1 AND created_by = $2
            """,
            name,
            user_id,
        )
        return dict(record) if record is not None else None

    async def list_by_user_with_count(self, user_id: int) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            WITH category_task_count AS (
                SELECT
                    category_id,
                    COUNT(*) as task_count
                FROM tasks.task
                WHERE owner_id = $1
                GROUP BY category_id
            )
            SELECT
                c.id,
                c.name,
                c.description,
                c.created_by,
                c.created_at,
                c.updated_at,
                COALESCE(ctc.task_count, 0) AS task_count
            FROM categories.category c
            LEFT JOIN category_task_count ctc ON c.id = ctc.category_id
            WHERE c.created_by = $1
            ORDER BY c.name ASC
            """,
            user_id,
        )
        return [dict(r) for r in records]

    async def update(
        self,
        category_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            UPDATE categories.category
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
            DELETE FROM categories.category
            WHERE id = $1
            """,
            category_id,
        )
        return result == "DELETE 1"
