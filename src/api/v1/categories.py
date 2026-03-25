from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from src.api.deps import get_current_user_id, get_category_service
from src.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from src.service.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: Annotated[CategoryCreate, Body()],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    return await category_service.create(category_in, current_user_id)


@router.get("")
async def list_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[CategoryOut]:
    return await category_service.list_by_user(current_user_id)


@router.get("/{category_id}")
async def get_category(
    category_id: Annotated[int, Path(ge=1)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    return await category_service.get_by_id(category_id, current_user_id)


@router.patch("/{category_id}")
async def update_category(
    category_id: Annotated[int, Path(ge=1)],
    category_update: Annotated[CategoryUpdate, Body()],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> CategoryOut:
    return await category_service.update(category_id, category_update, current_user_id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: Annotated[int, Path(ge=1)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
) -> None:
    await category_service.delete(category_id, current_user_id)
