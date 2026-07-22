from typing import Any

from shared.repository.base import BaseRepository


class ChatMessageRepository(BaseRepository):
    async def create(self, room_id: int, sender_id: int, content: str) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            INSERT INTO chats.chat_message (room_id, sender_id, content)
            VALUES ($1, $2, $3)
            RETURNING id, room_id, sender_id, content, created_at
            """,
            room_id,
            sender_id,
            content,
        )
        return dict(record) if record is not None else None

    async def list_by_room(self, room_id: int, limit: int, before_id: int | None) -> list[dict[str, Any]]:
        if before_id is not None:
            records = await self.fetch_all(
                """
                SELECT id, room_id, sender_id, content, created_at
                FROM chats.chat_message
                WHERE room_id = $1 AND id < $2
                ORDER BY id DESC
                LIMIT $3
                """,
                room_id,
                before_id,
                limit,
            )
        else:
            records = await self.fetch_all(
                """
                SELECT id, room_id, sender_id, content, created_at
                FROM chats.chat_message
                WHERE room_id = $1
                ORDER BY id DESC
                LIMIT $2
                """,
                room_id,
                limit,
            )
        return [dict(r) for r in records]
