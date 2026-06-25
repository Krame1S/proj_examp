from typing import Any

from shared.repository.base import BaseRepository


class AttachmentRepository(BaseRepository):
    async def create_attachment(
        self,
        task_id: int,
        owner_id: int,
        key: str,
        filename: str,
        content_type: str,
        size: int,  # actual byte count provided by the gateway
    ) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            INSERT INTO attachments.attachment (task_id, owner_id, key, filename, content_type, size)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, task_id, owner_id, key, filename, content_type, size, created_at, updated_at
            """,
            task_id,
            owner_id,
            key,
            filename,
            content_type,
            size,
        )
        return dict(record) if record is not None else None

    async def list_attachments_by_task(self, task_id: int) -> list[dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, task_id, owner_id, key, filename, content_type, size, created_at, updated_at
            FROM attachments.attachment
            WHERE task_id = $1
            ORDER BY created_at ASC
            """,
            task_id,
        )
        return [dict(r) for r in records]

    async def get_by_id(self, attachment_id: int) -> dict[str, Any] | None:
        record = await self.fetch_row(
            """
            SELECT id, task_id, owner_id, key, filename, content_type, size, created_at, updated_at
            FROM attachments.attachment
            WHERE id = $1
            """,
            attachment_id,
        )
        return dict(record) if record is not None else None

    async def delete_attachment(self, attachment_id: int, owner_id: int) -> bool:
        result = await self.execute(
            "DELETE FROM attachments.attachment WHERE id = $1 AND owner_id = $2",
            attachment_id,
            owner_id,
        )
        return result == "DELETE 1"
