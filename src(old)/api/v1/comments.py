from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from src.api.deps import get_comment_service, get_current_user_id
from src.schemas.comment import CommentIn, CommentOut
from src.service.comment import CommentService

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["comments"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_in: Annotated[CommentIn, Body()],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CommentOut:
    return await comment_service.create_comment(task_id, current_user_id, comment_in)


@router.get("", status_code=status.HTTP_200_OK)
async def list_comments(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[CommentOut]:
    return await comment_service.list_comments(task_id, current_user_id)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    task_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    comment_service: Annotated[CommentService, Depends(get_comment_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    await comment_service.delete_comment(comment_id, current_user_id)