from tag_service.core.database import get_db_pool
from tag_service.repository.tag import TagRepository
from tag_service.schemas.tag import TagCreate, TagOut, TagUpdate
from tag_service.exceptions.tag import TagAlreadyExists, TagNotFound


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    @classmethod
    async def create(cls) -> "TagService":
        pool = await get_db_pool()
        repo = TagRepository(pool)
        return cls(repository=repo)


    async def create_tag(self, tag_in: TagCreate, user_id: int) -> TagOut:
        existing = await self.repository.get_by_name(tag_in.name, user_id)
        if existing:
            raise TagAlreadyExists()

        record = await self.repository.create(
            name=tag_in.name,
            created_by=user_id,
        )
        return TagOut.from_db_row(record)


    async def get_tag_by_id(self, tag_id: int, user_id: int) -> TagOut:
        tag = await self.repository.get_by_id(tag_id, user_id)
        if tag is None:
            raise TagNotFound()
        return TagOut.from_db_row(tag)


    async def list_by_user(self, user_id: int) -> list[TagOut]:
        records = await self.repository.list_by_user(user_id)
        return [TagOut.from_db_row(r) for r in records]
        

    async def update_tag(
        self,
        tag_id: int,
        tag_update: TagUpdate,
        user_id: int,
    ) -> TagOut:
        tag = await self.repository.get_by_id(tag_id, user_id)
        if tag is None:
            raise TagNotFound()

        if tag_update.name is None or tag_update.name == tag["name"]:
            return TagOut.from_db_row(tag)

        existing = await self.repository.get_by_name(tag_update.name, user_id)
        if existing and existing["id"] != tag_id:
            raise TagAlreadyExists()

        updated = await self.repository.update(
            tag_id=tag_id,
            name=tag_update.name,
        )

        if updated is None:
            raise TagNotFound()

        return TagOut.from_db_row(updated)


    async def delete_tag(self, tag_id: int, user_id: int) -> None:
        tag = await self.repository.get_by_id(tag_id, user_id)
        if tag is None:
            raise TagNotFound()

        deleted = await self.repository.delete(tag_id)
        if not deleted:
            raise TagNotFound()