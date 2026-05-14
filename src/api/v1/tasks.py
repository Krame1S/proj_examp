from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, status

from src.api.deps import get_current_user_id, get_task_service
from src.models.task import TaskStatus
from src.schemas.task import TaskIn, TaskOut, TaskUpdate, GetTaskResponse
from src.service.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: Annotated[TaskIn, Body()],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    return await task_service.create_task(task_in, current_user_id)


@router.get("", status_code=status.HTTP_200_OK)
async def list_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    category_id: Annotated[Optional[int], Query(ge=1)] = None,
    tag_ids: Annotated[Optional[list[int]], Query()] = None,
    status_filter: Annotated[Optional[TaskStatus], Query(alias="status")] = None,
) -> GetTaskResponse:
    return await task_service.list_tasks(
        owner_id=current_user_id,
        limit=limit,
        category_id=category_id,
        tag_ids=tag_ids,
        status_filter=status_filter,
    )


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    return await task_service.get_task_by_id(current_user_id, task_id)


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def patch_task(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    update_data: Annotated[TaskUpdate, Body()],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    return await task_service.patch_task(
        task_id=task_id,
        update_data=update_data,
        user_id=current_user_id,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    return await task_service.delete_task(task_id, current_user_id)