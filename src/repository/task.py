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

    # async def get_by_email(self, email: str) -> asyncpg.Record | None:
    #     return await self.fetch_row(
    #         """
    #         SELECT id, email, password_hash, is_active, created_at
    #         FROM "user"
    #         WHERE email = $1
    #         """,
    #         email,
    #     )

    # async def update_email(self, user_id: int, email: str) -> asyncpg.Record | None:
    #     return await self.fetch_row(
    #         """
    #         UPDATE "user"
    #         SET email = $2, updated_at = NOW()
    #         WHERE id = $1
    #         RETURNING id, email, is_active, created_at
    #         """,
    #         user_id,
    #         email,
    #     )

    # async def delete(self, user_id: int) -> bool:
    #     result = await self.execute(
    #         """
    #         DELETE FROM "user"
    #         WHERE id = $1
    #         """,
    #         user_id,
    #     )
    #     return result == "DELETE 1"

