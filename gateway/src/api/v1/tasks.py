import json
from src.api.deps import get_current_user_id
from src.schemas.task import TaskIn, TaskOut, TaskStatus, TaskUpdate, GetTaskResponse
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, status
from src.broker.rpc_publisher import rpc_publisher
from shared.broker.queues import ConsumerQueue
from typing import Annotated, Optional

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: Annotated[TaskIn, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**task_in.model_dump(), "user_id": user_id}),
        request_queue_name=ConsumerQueue.TASK_CREATE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TaskOut.model_validate(data)


@router.get("", status_code=status.HTTP_200_OK)
async def list_tasks(
    user_id: Annotated[int, Depends(get_current_user_id)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    category_id: Annotated[Optional[int], Query(ge=1)] = None,
    tag_ids: Annotated[Optional[list[int]], Query()] = None,
    status_filter: Annotated[Optional[TaskStatus], Query(alias="status")] = None,
) -> GetTaskResponse:
    raw = await rpc_publisher.call(
        message=json.dumps({
            "user_id": user_id,
            "limit": limit,
            "category_id": category_id,
            "tag_ids": tag_ids,
            "status_filter": status_filter.value if status_filter else None,
        }),
        request_queue_name=ConsumerQueue.TASK_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return GetTaskResponse.model_validate(data)


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"task_id": task_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.TASK_GET_BY_ID.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TaskOut.model_validate(data)


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def patch_task(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    update_data: Annotated[TaskUpdate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TaskOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"task_id": task_id, "user_id": user_id, **update_data.model_dump()}),
        request_queue_name=ConsumerQueue.TASK_PATCH.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )
    return TaskOut.model_validate(data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps({"task_id": task_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.TASK_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(
            status_code=data["error"]["status_code"],
            detail=data["error"],
        )