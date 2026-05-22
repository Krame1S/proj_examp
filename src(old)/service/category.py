from src.exceptions.category import CategoryNotFound, CategoryAlreadyExists
from src.repository.category import CategoryRepository
from src.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository


    async def create(self, category_in: CategoryCreate, user_id: int) -> CategoryOut:
        existing = await self.repository.get_by_name(category_in.name, user_id)
        if existing:
            raise CategoryAlreadyExists()

        record = await self.repository.create(
            name=category_in.name,
            description=category_in.description,
            created_by=user_id,
        )
        return CategoryOut.from_db_row(record)


    async def get_by_id(self, category_id: int, user_id: int) -> CategoryOut:
        category = await self.repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()
        return CategoryOut.from_db_row(category)


    async def list_by_user(self, user_id: int) -> list[CategoryOut]:
        records = await self.repository.list_by_user_with_count(user_id)
        return [CategoryOut.from_db_row(r) for r in records]


    async def update(
        self,
        category_id: int,
        category_update: CategoryUpdate,
        user_id: int,
    ) -> CategoryOut:
        category = await self.repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()

        updated = await self.repository.update(
            category_id=category_id,
            name=category_update.name,
            description=category_update.description,
        )

        if updated is None:
            raise CategoryNotFound()

        return CategoryOut.from_db_row(updated)


    async def delete(self, category_id: int, user_id: int) -> None:
        category = await self.repository.get_by_id(category_id, user_id)
        if category is None:
            raise CategoryNotFound()

        deleted = await self.repository.delete(category_id)
        if not deleted:
            raise CategoryNotFound()