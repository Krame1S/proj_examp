from typing import Optional

from category_service.core.database import get_db_pool
from category_service.exceptions.category import CategoryAlreadyExists, CategoryNotFound
from category_service.repository.category import CategoryRepository
from category_service.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepository,
    ):
        self.repository = repository

    @classmethod
    async def create(cls) -> "CategoryService":
        pool = await get_db_pool()
        return cls(repository=CategoryRepository(pool))

    async def create_category(self, request: CategoryCreate, owner_id: int) -> CategoryOut:
        existing = await self.repository.get_by_name(request.name, owner_id)
        if existing:
            raise CategoryAlreadyExists()

        record = await self.repository.create(
            name=request.name,
            description=request.description,
            created_by=owner_id,
        )
        return CategoryOut.from_db_row(record)

    async def list_categories(
        self,
        owner_id: int,
        limit: int = 100,
        parent_id: Optional[int] = None,
    ) -> list[CategoryOut]:
        records = await self.repository.list_by_user_with_count(owner_id)
        categories = records[:limit]
        return [CategoryOut.from_db_row(record) for record in categories]

    async def get_category_by_id(self, owner_id: int, category_id: int) -> CategoryOut:
        category = await self.repository.get_by_id(category_id, owner_id)
        if category is None:
            raise CategoryNotFound()
        return CategoryOut.from_db_row(category)

    async def patch_category(
        self,
        category_id: int,
        update_data: CategoryUpdate,
        user_id: int,
    ) -> CategoryOut:
        category = await self.repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()

        updated = await self.repository.update(
            category_id=category_id,
            name=update_data.name,
            description=update_data.description,
        )
        if updated is None:
            raise CategoryNotFound()
        return CategoryOut.from_db_row(updated)

    async def delete_category(self, category_id: int, user_id: int) -> None:
        category = await self.repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()

        deleted = await self.repository.delete(category_id)
        if not deleted:
            raise CategoryNotFound()
