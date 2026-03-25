from typing import Any, Dict, List, Optional

import asyncpg

from src.repository.base import BaseRepository


class TaskRepository(BaseRepository):

    async def create_task(
        self,
        title: str,
        description: str,
        owner_id: int,
        category_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        record = await self.fetch_row(
            """
            INSERT INTO task (title, description, owner_id, category_id)
            VALUES ($1, $2, $3, $4)
            RETURNING id, title, description, owner_id, category_id, is_active, created_at, updated_at
            """,
            title,
            description,
            owner_id,
            category_id,
        )
        if record is None:
            raise RuntimeError("Task creation failed - no row returned")
        return dict(record)


    async def get_task_by_id(self, task_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT 
                t.id, t.title, t.description, t.owner_id, t.category_id, t.is_active,
                t.created_at, t.updated_at,
                c.name AS category_name
            FROM task t
            LEFT JOIN category c ON t.category_id = c.id
            WHERE t.id = $1 AND t.owner_id = $2
            """,
            task_id,
            owner_id,
        )
        return dict(record) if record is not None else None


    async def list_all_tasks(
        self, owner_id: int, skip: int = 0, limit: int = 20
    ) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT 
                t.id, t.title, t.description, t.owner_id, t.category_id, t.is_active,
                t.created_at, t.updated_at,
                c.name AS category_name
            FROM task t
            LEFT JOIN category c ON t.category_id = c.id
            WHERE t.owner_id = $1
            ORDER BY t.created_at DESC
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
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
        category_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            UPDATE task t
            SET 
                title = COALESCE($1, t.title),
                description = COALESCE($2, t.description),
                is_active = COALESCE($3, t.is_active),
                category_id = COALESCE($4, t.category_id),
                updated_at = NOW()
            FROM task t2
            LEFT JOIN category c ON t2.category_id = c.id
            WHERE t.id = $5
            RETURNING 
                t.id, t.title, t.description, t.owner_id, t.category_id, t.is_active, 
                t.created_at, t.updated_at,
                c.name AS category_name
            """,
            title,
            description,
            is_active,
            category_id,
            task_id,
        )
        return dict(record) if record is not None else None


    async def delete_task(self, task_id: int) -> bool:
        result = await self.execute(
            "DELETE FROM task WHERE id = $1",
            task_id,
        )
        return result == "DELETE 1"