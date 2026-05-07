from typing import Any, Dict, List, Optional
from src.repository.base import BaseRepository


class TaskRepository(BaseRepository):

    async def create_task(
        self,
        title: str,
        description: str,
        owner_id: int,
        category_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            WITH inserted_task AS (
                INSERT INTO task (title, description, owner_id, category_id)
                VALUES ($1, $2, $3, $4)
                RETURNING id, title, description, owner_id, category_id, is_active, created_at, updated_at
            )
            SELECT
                task.id,
                task.title,
                task.description,
                task.owner_id,
                task.category_id,
                task.is_active,
                task.created_at,
                task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM inserted_task AS task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            GROUP BY task.id, task.title, task.description, task.owner_id,
                    task.category_id, task.is_active, task.created_at,
                    task.updated_at, category.name
            """,
            title,
            description,
            owner_id,
            category_id,
        )
        return dict(record) if record is not None else None


    async def get_task_by_id(self, task_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id, task.is_active,
                task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            WHERE task.id = $1 AND task.owner_id = $2
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.is_active, task.created_at, task.updated_at, category.name
            """,
            task_id,
            owner_id,
        )
        return dict(record) if record is not None else None


    async def list_all_tasks(
        self, owner_id: int, limit: int
    ) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id, task.is_active,
                task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            WHERE task.owner_id = $1
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.is_active, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $2
            """,
            owner_id,
            limit,
        )
        return [dict(r) for r in records]


    async def list_all_tasks_by_category(
        self,
        owner_id: int,
        category_id: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id, task.is_active,
                task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            WHERE task.owner_id = $1 AND task.category_id = $2
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.is_active, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $3
            """,
            owner_id,
            category_id,
            limit,
        )
        return [dict(r) for r in records]


    async def patch_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
        category_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        await self.fetch_row(
            """
            UPDATE task
            SET
                title = COALESCE($1, title),
                description = COALESCE($2, description),
                is_active = COALESCE($3, is_active),
                category_id = COALESCE($4, category_id),
                updated_at = NOW()
            WHERE id = $5
            """,
            title,
            description,
            is_active,
            category_id,
            task_id,
        )

        record = await self.fetch_row(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id, task.is_active,
                task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            WHERE task.id = $1
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.is_active, task.created_at, task.updated_at, category.name
            """,
            task_id,
        )
        return dict(record) if record is not None else None


    async def delete_task(self, task_id: int) -> bool:
        result = await self.execute(
            "DELETE FROM task WHERE id = $1",
            task_id,
        )
        return result == "DELETE 1"


    async def set_tags_on_task(
        self,
        task_id: int,
        owner_id: int,
        tag_ids: List[int],
    ) -> None:
        await self.execute(
            """
            WITH
            validated_tags AS (
                SELECT id FROM tag
                WHERE id = ANY($2::bigint[]) AND created_by = $3
            ),
            inserted_new_task_tag AS (
                INSERT INTO task_tag (task_id, tag_id)
                SELECT $1, id FROM validated_tags
                WHERE id NOT IN (SELECT tag_id FROM task_tag WHERE task_id = $1)
                ON CONFLICT DO NOTHING
                RETURNING tag_id
            ),
            deleted_old_task_tag AS (
                DELETE FROM task_tag
                WHERE task_id = $1
                AND tag_id NOT IN (SELECT id FROM validated_tags)
                RETURNING tag_id
            )
            SELECT
                (SELECT ARRAY_AGG(tag_id) FROM inserted_new_task_tag) AS added,
                (SELECT ARRAY_AGG(tag_id) FROM deleted_old_task_tag) AS removed
            """,
            task_id,
            tag_ids,
            owner_id,
        )

    async def list_all_tasks_by_tags(
        self,
        owner_id: int,
        tag_ids: list[int],
        limit: int,
    ) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id, task.is_active,
                task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tag.name) FILTER (WHERE tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tag ON task_tag.tag_id = tag.id
            WHERE task.owner_id = $1
            AND task.id IN (
                SELECT task_tag.task_id FROM task_tag
                WHERE task_tag.tag_id = ANY($2::bigint[])
                GROUP BY task_tag.task_id
                HAVING COUNT(DISTINCT task_tag.tag_id) = array_length($2::bigint[], 1)
            )
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                    task.is_active, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $3
            """,
            owner_id,
            tag_ids,
            limit,
        )
        return [dict(r) for r in records]