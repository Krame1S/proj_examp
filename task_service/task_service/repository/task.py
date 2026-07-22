from typing import Any

from shared.repository.base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_task(
        self,
        title: str,
        description: str,
        owner_id: int,
        category_id: int | None = None,
        status: str = "todo",
    ) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            WITH inserted_task AS (
                INSERT INTO task (title, description, owner_id, category_id, status)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, title, description, owner_id, category_id, status, created_at, updated_at
            )
            SELECT
                task.id,
                task.title,
                task.description,
                task.owner_id,
                task.category_id,
                task.status,
                task.created_at,
                task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM inserted_task AS task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            GROUP BY task.id, task.title, task.description, task.owner_id,
                    task.category_id, task.status, task.created_at,
                    task.updated_at, category.name
            """,
            title,
            description,
            owner_id,
            category_id,
            status,
        )
        return dict(record) if record is not None else None

    async def get_task_by_id(self, task_id: int, owner_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id,
                task.status, task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            WHERE task.id = $1 AND task.owner_id = $2
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.status, task.created_at, task.updated_at, category.name
            """,
            task_id,
            owner_id,
        )
        return dict(record) if record is not None else None

    async def list_all_tasks(self, owner_id: int, limit: int, status: str | None = None) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id,
                task.status, task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            WHERE task.owner_id = $1
              AND ($3::text IS NULL OR task.status::text = $3::text)
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.status, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $2
            """,
            owner_id,
            limit,
            status,
        )
        return [dict(r) for r in records]

    async def list_all_tasks_by_category(
        self,
        owner_id: int,
        category_id: int,
        limit: int,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id,
                task.status, task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            WHERE task.owner_id = $1 AND task.category_id = $2
              AND ($4::text IS NULL OR task.status::text = $4::text)
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.status, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $3
            """,
            owner_id,
            category_id,
            limit,
            status,
        )
        return [dict(r) for r in records]

    async def patch_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ) -> dict[str, Any] | None:
        await self.fetch_row(
            """
            UPDATE task
            SET
                title = COALESCE($1, title),
                description = COALESCE($2, description),
                category_id = COALESCE($3, category_id),
                status = COALESCE($4, status),
                updated_at = NOW()
            WHERE id = $5
            """,
            title,
            description,
            category_id,
            status,
            task_id,
        )

        record = await self.fetch_row(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id,
                task.status, task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            WHERE task.id = $1
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                     task.status, task.created_at, task.updated_at, category.name
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
        tag_ids: list[int],
    ) -> None:
        await self.execute(
            """
            WITH
            validated_tags AS (
                SELECT id FROM tags.tag
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
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT
                task.id, task.title, task.description, task.owner_id, task.category_id,
                task.status, task.created_at, task.updated_at,
                category.name AS category_name,
                COALESCE(ARRAY_AGG(tags.tag.name) FILTER (WHERE tags.tag.id IS NOT NULL), ARRAY[]::text[]) AS tags
            FROM task
            LEFT JOIN categories.category ON task.category_id = category.id
            LEFT JOIN task_tag ON task.id = task_tag.task_id
            LEFT JOIN tags.tag ON task_tag.tag_id = tags.tag.id
            WHERE task.owner_id = $1
            AND ($4::text IS NULL OR task.status::text = $4::text)
            AND task.id IN (
                SELECT task_tag.task_id FROM task_tag
                WHERE task_tag.tag_id IN (SELECT UNNEST($2::bigint[]))
                GROUP BY task_tag.task_id
                HAVING COUNT(DISTINCT task_tag.tag_id) = array_length($2::bigint[], 1)
            )
            GROUP BY task.id, task.title, task.description, task.owner_id, task.category_id,
                    task.status, task.created_at, task.updated_at, category.name
            ORDER BY task.created_at DESC
            LIMIT $3
            """,
            owner_id,
            tag_ids,
            limit,
            status,
        )
        return [dict(r) for r in records]

    async def get_valid_tag_ids(self, tag_ids: list[int], owner_id: int) -> list[int]:
        records = await self.fetch_all(
            """
            SELECT id FROM tags.tag
            WHERE id = ANY($1::bigint[]) AND created_by = $2
            """,
            tag_ids,
            owner_id,
        )
        return [r["id"] for r in records]

    async def get_status_counts(self, owner_id: int) -> dict:
        records = await self.fetch_all(
            """
            SELECT status, COUNT(*) as count
            FROM task
            WHERE owner_id = $1
            GROUP BY status
            """,
            owner_id,
        )
        counts = {"todo": 0, "in_progress": 0, "done": 0, "cancelled": 0}
        for r in records:
            counts[r["status"]] = r["count"]
        return counts
