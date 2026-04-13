from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from src.api.deps import get_current_user_id, get_tag_service
from src.schemas.tag import TagCreate, TagOut, TagUpdate
from src.service.tag import TagService

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: Annotated[TagCreate, Body()],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    return await tag_service.create(tag_in, current_user_id)


@router.get("")
async def list_tags(
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[TagOut]:
    return await tag_service.list_by_user(current_user_id)


@router.get("/{tag_id}")
async def get_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    return await tag_service.get_by_id(tag_id, current_user_id)


@router.patch("/{tag_id}")
async def update_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    tag_update: Annotated[TagUpdate, Body()],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> TagOut:
    return await tag_service.update(tag_id, tag_update, current_user_id)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: Annotated[int, Path(ge=1, le=999_999_999_999)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    await tag_service.delete(tag_id, current_user_id)