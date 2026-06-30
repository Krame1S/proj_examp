from typing import Any

from shared.repository.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        record = await self.fetch_row(
            'SELECT id FROM users."user" WHERE email = $1',
            email,
        )
        return dict(record) if record is not None else None
