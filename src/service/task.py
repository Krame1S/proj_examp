from typing import Optional

from src.exceptions.task import TaskNotFound, TaskNotOwned
from src.repository.task import TaskRepository
from src.schemas.task import TaskIn, TaskOut, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def _get_task_or_raise(self, task_id: int, owner_id: int) -> dict:
        task = await self.repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()
        return task

    async def create_task(self, task_in: TaskIn, owner_id: int) -> TaskOut:
        record = await self.repository.create_task(
            title=task_in.title,
            description=task_in.description,
            owner_id=owner_id,
        )
        return TaskOut.from_db_row(record)

    async def list_tasks(self, owner_id: int) -> list[TaskOut]:
        records = await self.repository.list_all_tasks(owner_id)
        return [TaskOut.from_db_row(r) for r in records]

    async def get_task_by_id(self, owner_id: int, task_id: int) -> TaskOut:
        record = await self._get_task_or_raise(task_id, owner_id)
        return TaskOut.from_db_row(record)

    async def patch_task(
        self,
        task_id: int,
        update_data: TaskUpdate,
        user_id: int,
    ) -> TaskOut:
        task = await self._get_task_or_raise(task_id, user_id)

        if task["owner_id"] != user_id:
            raise TaskNotOwned()

        changes = update_data.model_dump(exclude_unset=True)
        if not changes:
            return TaskOut.from_db_row(task)

        new_values = {
            "title": changes.get("title", task["title"]),
            "description": changes.get("description", task["description"]),
            "is_active": changes.get("is_active", task["is_active"]),
        }

        updated = await self.repository.patch_task(
            task_id=task_id,
            title=new_values["title"],
            description=new_values["description"],
            is_active=new_values["is_active"],
        )

        if updated is None:
            raise TaskNotFound("Task disappeared during update")

        return TaskOut.from_db_row(updated)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self._get_task_or_raise(task_id,  user_id)

        if task["owner_id"] != user_id:
            raise TaskNotOwned()

        deleted = await self.repository.delete_task(task_id)
        if not deleted:
            raise TaskNotFound("Task was already deleted")