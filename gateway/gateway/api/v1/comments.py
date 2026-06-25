import json
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from gateway.api.deps import get_current_user_id
from gateway.broker.rpc_publisher import rpc_publisher
from shared.contracts.comment.contracts import CommentIn, CommentOut
from shared.broker.queues import ConsumerQueue

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["comments"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_in: Annotated[CommentIn, Body()],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> CommentOut:
    raw = await rpc_publisher.call(
        message=json.dumps({**comment_in.model_dump(), "task_id": task_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.COMMENT_CREATE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return CommentOut.model_validate(data)


@router.get("", status_code=status.HTTP_200_OK)
async def list_comments(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[CommentOut]:
    raw = await rpc_publisher.call(
        message=json.dumps({"task_id": task_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.COMMENT_LIST.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])
    return [CommentOut.model_validate(c) for c in data]


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    raw = await rpc_publisher.call(
        message=json.dumps({"comment_id": comment_id, "task_id": task_id, "user_id": user_id}),
        request_queue_name=ConsumerQueue.COMMENT_DELETE.value,
    )
    data = json.loads(raw)
    if "error" in data:
        raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"])