from alembic.environment import Optional
from asyncpg.exceptions import UniqueViolationError
from shared.contracts.auth.contracts import UserProfile

from user_service.core.database import get_db_pool
from user_service.exceptions.user import EmailAlreadyTaken, UserNotFound
from user_service.repository.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @classmethod
    async def create(cls) -> "UserService":
        pool = await get_db_pool()
        return cls(UserRepository(pool))

    async def _get_user_or_raise(self, user_id: int) -> dict:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound
        return user

    async def get_profile(self, user_id: int) -> UserProfile:
        user = await self._get_user_or_raise(user_id)
        return UserProfile.from_db_row(user)

    async def update_email(self, user_id: int, email: Optional[str]) -> UserProfile:
        if email is None:
            return await self.get_profile(user_id)
        try:
            updated = await self.repository.update_email(user_id, email)
        except UniqueViolationError as e:
            raise EmailAlreadyTaken from e
        if updated is None:
            raise UserNotFound
        return UserProfile.from_db_row(updated)

    async def delete(self, user_id: int) -> None:
        deleted = await self.repository.delete(user_id)
        if not deleted:
            raise UserNotFound
