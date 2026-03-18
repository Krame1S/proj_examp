import asyncpg

from src.repository.base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_task(self, title: str, description: str, owner_id: int) -> asyncpg.Record:
        result = await self.fetch_row(
            """
            INSERT INTO "task" (title, description, owner_id)
            VALUES ($1, $2, $3)
            RETURNING id, title, description, owner_id, is_active, created_at
            """,
            title,
            description,
            owner_id,
        )
        if result is None:
            raise ValueError("Failed to create task")
        return result

    async def list_all_tasks(self, user_id: int) -> list[asyncpg.Record] | None:
        return await self.fetch_all(
            """
            SELECT id, title, description, owner_id, is_active, created_at, updated_at
            FROM "task"
            WHERE owner_id = $1
            """,
            user_id,
        )

    async def get_task_by_id(self, task_id: int) -> asyncpg.Record | None:
        return await self.fetch_row(
            """
            SELECT id, title, description, owner_id, is_active, created_at, updated_at
            FROM task
            WHERE id = $1
            """,
            task_id
        )


    async def patch_task(
        self,
        task_id: int,
        title: str,
        description: str,
        is_active: bool
    ) -> asyncpg.Record | None:
        return await self.fetch_row(
            """
            UPDATE task
            SET title       = $1,
                description = $2,
                is_active   = $3,
                updated_at  = NOW()
            WHERE id = $4
        RETURNING id, title, description, owner_id, is_active, created_at, updated_at
            """,
            title, description, is_active, task_id
        )

    async def delete_task(self, task_id: int) -> bool:
        result = await self.execute(
            """
            DELETE FROM task
            WHERE id = $1
            """,
            task_id,
        )
        return result == "DELETE 1"