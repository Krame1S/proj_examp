import json
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from gateway.api.deps import get_current_user_id
from gateway.broker.rpc_publisher import rpc_publisher
from shared.contracts.category.contracts import CategoryCreate, CategoryOut, CategoryUpdate
from shared.broker.queues import ConsumerQueue

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: Annotated[CategoryCreate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**category_in.model_dump(), "user_id": user_id}),
        request_queue_name=ConsumerQueue.CATEGORY_CREATE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return CategoryOut.model_validate(data)


@router.get("", status_code=status.HTTP_200_OK)
async def list_categories(
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[CategoryOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id}),
        request_queue_name=ConsumerQueue.CATEGORY_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return [CategoryOut.model_validate(c) for c in data]


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(
    category_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"category_id": category_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CATEGORY_GET_BY_ID.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return CategoryOut.model_validate(data)


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(
    category_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    category_update: Annotated[CategoryUpdate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**category_update.model_dump(), "category_id": category_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CATEGORY_PATCH.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return CategoryOut.model_validate(data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps({"category_id": category_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.CATEGORY_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])