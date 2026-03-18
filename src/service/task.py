from src.repository.task import TaskRepository
from src.schemas.task import TaskIn, TaskOut


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
            is_active=record["is_active"],
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
                is_active=record["is_active"],
            )
            for record in records
        ]

