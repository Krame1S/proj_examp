from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from src.api.deps import get_current_user_id, get_task_service
from src.schemas.task import TaskIn, TaskOut, TaskUpdate
from src.service.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: Annotated[TaskIn, Body],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)]
) -> TaskOut:
    return await task_service.create_task(task_in, current_user_id)


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)]
) -> list[TaskOut]:
    return await task_service.list_tasks(current_user_id)


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
async def patch_task(
    task_id: Annotated[int, Path(ge=1)],
    update_data: Annotated[TaskUpdate, Body()],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)]
) -> TaskOut:
    return await task_service.patch_task(
        task_id=task_id,
        update_data=update_data,
        user_id=current_user_id
    )

