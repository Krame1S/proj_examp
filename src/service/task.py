from typing import Any

from fastapi import HTTPException, status

from src.repository.task import TaskRepository
from src.schemas.task import TaskIn, TaskOut, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task_in: TaskIn, owner_id: int) -> TaskOut:
        record = await self.repository.create_task(
            title=task_in.title,
            description=task_in.description,
            owner_id=owner_id
        )
        return TaskOut(
            id=record["id"],
            title=record["title"],
            description=record["description"],
            owner_id=record["owner_id"],
            is_active=bool(record["is_active"]),
            created_at=str(record["created_at"]),
            updated_at=str(record["updated_at"]),
        )

    async def patch_task(
        self,
        task_id: int,
        update_data: TaskUpdate,
        user_id: int
    ) -> TaskOut:
        task = await self.repository.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

        if task["owner_id"] != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task")

        # Only build what we actually want to change
        update_map = update_data.model_dump(exclude_unset=True)
        if not update_map:
            return TaskOut(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                owner_id=task["owner_id"],
                is_active=task["is_active"],
                created_at=task["created_at"].isoformat() if task["created_at"] else None,
                updated_at=task["updated_at"].isoformat() if task["updated_at"] else None,
            )

        new_title = update_map.get("title", task["title"])
        new_desc = update_map.get("description", task["description"])
        new_active = update_map.get("is_active", task["is_active"])

        updated = await self.repository.patch_task(
            task_id,
            title=new_title,
            description=new_desc,
            is_active=new_active
        )

        if not updated:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Task disappeared during update")

        return TaskOut(
            id=updated["id"],
            title=updated["title"],
            description=updated["description"],
            owner_id=updated["owner_id"],
            is_active=updated["is_active"],
            created_at=updated["created_at"].isoformat() if updated["created_at"] else None,
            updated_at=updated["updated_at"].isoformat() if updated["updated_at"] else None,
        )

    async def list_tasks(self, owner_id: int) -> list[TaskOut]:
        records = await self.repository.list_all_tasks(owner_id)
        if records is None:
            return []
        return [
            TaskOut(
                id=record["id"],
                title=record["title"],
                description=record["description"],
                owner_id=record["owner_id"],
                is_active=bool(record["is_active"]),
                created_at=str(record["created_at"]),
                updated_at=str(record["updated_at"]),
            )
            for record in records
        ]

    async def delete_task(
        self,
        task_id: int,
        user_id: int
    ) -> None:
        task = await self.repository.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
        if task["owner_id"] != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task")

        await self.repository.delete_task(task_id)