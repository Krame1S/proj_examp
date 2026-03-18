from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from src.api.deps import get_current_user_id, get_task_service
from src.schemas.task import TaskIn, TaskOut
from src.service.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: Annotated[TaskIn, Body],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)]
) -> TaskOut:
    return await task_service.create_task(task_in, current_user_id)

