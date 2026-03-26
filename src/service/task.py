from typing import Optional

from src.exceptions.category import CategoryNotFound
from src.exceptions.task import TaskNotFound
from src.repository.category import CategoryRepository
from src.repository.task import TaskRepository
from src.schemas.task import TaskIn, TaskOut, TaskUpdate


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository,
    ):
        self.task_repository = task_repository
        self.category_repository = category_repository

    async def _get_task_or_raise(self, task_id: int, owner_id: int) -> dict:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()
        return task

    async def _validate_category_belongs_to_user(self, category_id: Optional[int], user_id: int) -> None:
        if category_id is None:
            return

        category = await self.category_repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()


    async def create_task(self, task_in: TaskIn, owner_id: int) -> TaskOut:
        await self._validate_category_belongs_to_user(task_in.category_id, owner_id)

        record = await self.task_repository.create_task(
            title=task_in.title,
            description=task_in.description,
            owner_id=owner_id,
            category_id=task_in.category_id,
        )
        return TaskOut.from_db_row(record)


    async def list_tasks(
        self, 
        owner_id: int, 
        skip: int = 0, 
        limit: int = 20,
        category_id: Optional[int] = None
    ) -> list[TaskOut]:
        if category_id is not None:
            await self._validate_category_belongs_to_user(category_id, owner_id)
            
            records = await self.task_repository.list_all_tasks_by_category(
                owner_id=owner_id, 
                category_id=category_id,
                skip=skip, 
                limit=limit
            )
        else:
            records = await self.task_repository.list_all_tasks(
                owner_id=owner_id, skip=skip, limit=limit
            )
        
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

        changes = update_data.model_dump(exclude_unset=True)
        if not changes:
            return TaskOut.from_db_row(task)

        if "category_id" in changes:
            await self._validate_category_belongs_to_user(changes["category_id"], user_id)

        updated = await self.task_repository.patch_task(
            task_id=task_id,
            title=changes.get("title"),
            description=changes.get("description"),
            is_active=changes.get("is_active"),
            category_id=changes.get("category_id"),
        )

        if updated is None:
            raise TaskNotFound()

        return TaskOut.from_db_row(updated)


    async def delete_task(self, task_id: int, user_id: int) -> None:
        await self._get_task_or_raise(task_id, user_id)
        deleted = await self.task_repository.delete_task(task_id)
        if not deleted:
            raise TaskNotFound()