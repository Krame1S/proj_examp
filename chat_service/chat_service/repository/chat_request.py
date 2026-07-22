from typing import Any

from shared.repository.base import BaseRepository


class ChatRequestRepository(BaseRepository):
    async def create(self, requester_id: int, target_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            INSERT INTO chats.chat_request (requester_id, target_id)
            VALUES ($1, $2)
            RETURNING id, requester_id, target_id, status, created_at, updated_at
            """,
            requester_id,
            target_id,
        )
        return dict(record) if record is not None else None

    async def list_by_user(self, user_id: int, direction: str, status: str | None = None) -> list[dict[str, Any]]:
        where = "requester_id = $1" if direction == "outgoing" else "target_id = $1"

        if status is not None:
            where += " AND status = $2"
            records = await self.fetch_all(
                f"""
                SELECT id, requester_id, target_id, status, created_at, updated_at
                FROM chats.chat_request
                WHERE {where}
                ORDER BY created_at DESC
                """,
                user_id,
                status,
            )
        else:
            records = await self.fetch_all(
                f"""
                SELECT id, requester_id, target_id, status, created_at, updated_at
                FROM chats.chat_request
                WHERE {where}
                ORDER BY created_at DESC
                """,
                user_id,
            )
        return [dict(r) for r in records]

    async def get_by_id(self, request_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT id, requester_id, target_id, status, created_at, updated_at
            FROM chats.chat_request
            WHERE id = $1
            """,
            request_id,
        )
        return dict(record) if record is not None else None

    async def update_status(self, request_id: int, status: str) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            UPDATE chats.chat_request
            SET status = $1, updated_at = now()
            WHERE id = $2
            RETURNING id, requester_id, target_id, status, created_at, updated_at
            """,
            status,
            request_id,
        )
        return dict(record) if record is not None else None

    async def list_accepted_by_user(self, user_id: int) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, requester_id, target_id, status, created_at, updated_at
            FROM chats.chat_request
            WHERE (requester_id = $1 OR target_id = $1) AND status = 'accepted'
            ORDER BY updated_at DESC
            """,
            user_id,
        )
        return [dict(r) for r in records]

    async def get_active_between(self, requester_id: int, target_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT id FROM chats.chat_request
            WHERE requester_id = $1 AND target_id = $2 AND status = 'pending'
            """,
            requester_id,
            target_id,
        )
        return dict(record) if record is not None else None
