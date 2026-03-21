from typing import Any, Dict, List, Optional

import asyncpg

from src.repository.base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_task(
        self,
        title: str,
        description: str,
        owner_id: int,
    ) -> Dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO task (title, description, owner_id)
            VALUES ($1, $2, $3)
            RETURNING id, title, description, owner_id, is_active, created_at, updated_at
            """,
            title,
            description,
            owner_id,
        )
        if record is None:
            raise RuntimeError("Task creation failed - no row returned")
        return dict(record)


    async def get_task_by_id(self, task_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id, title, description, owner_id, is_active, created_at, updated_at
            FROM task
            WHERE id = $1 AND owner_id = $2
            """,
            task_id,
            owner_id
        )
        return dict(record) if record is not None else None


    async def list_all_tasks(self, owner_id: int, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, title, description, owner_id, is_active, created_at, updated_at
            FROM task
            WHERE owner_id = $1
            ORDER BY created_at DESC
            OFFSET $2 LIMIT $3
            """,
            owner_id,
            skip,
            limit,
        )
        return [dict(r) for r in records]


    async def patch_task(
        self,
        task_id: int,
        title: str,
        description: str,
        is_active: bool,
    ) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            UPDATE task
            SET title = $1, description = $2, is_active = $3, updated_at = NOW()
            WHERE id = $4
            RETURNING id, title, description, owner_id, is_active, created_at, updated_at
            """,
            title, description, is_active, task_id
        )
        return dict(record) if record is not None else None


    async def delete_task(self, task_id: int) -> bool:
        result = await self.execute(
            "DELETE FROM task WHERE id = $1",
            task_id,
        )
        return result == "DELETE 1"