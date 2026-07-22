import json
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from shared.broker.queues import ConsumerQueue
from shared.contracts.tag.contracts import TagCreate, TagOut, TagUpdate

from gateway.api.deps import get_current_user_id
from gateway.broker.rpc_publisher import rpc_publisher

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: Annotated[TagCreate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**tag_in.model_dump(), "user_id": user_id}),
        request_queue_name=ConsumerQueue.TAG_CREATE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return TagOut.model_validate(data)


@router.get("", status_code=status.HTTP_200_OK)
async def list_tags(
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[TagOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"user_id": user_id}),
        request_queue_name=ConsumerQueue.TAG_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return [TagOut.model_validate(t) for t in data]


@router.get("/{tag_id}", status_code=status.HTTP_200_OK)
async def get_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    raw = await rpc_publisher.call(
        message=json.dumps({"tag_id": tag_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.TAG_GET_BY_ID.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return TagOut.model_validate(data)


@router.put("/{tag_id}", status_code=status.HTTP_200_OK)
async def update_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    tag_update: Annotated[TagUpdate, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**tag_update.model_dump(), "tag_id": tag_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.TAG_PATCH.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return TagOut.model_validate(data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps({"tag_id": tag_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.TAG_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
