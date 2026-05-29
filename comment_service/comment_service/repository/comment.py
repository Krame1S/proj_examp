from typing import Any, Dict, List, Optional
from comment_service.repository.base import BaseRepository


class CommentRepository(BaseRepository):

    async def create_comment(self, content: str, task_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            INSERT INTO comments.comment (content, task_id, owner_id)
            VALUES ($1, $2, $3)
            RETURNING id, content, task_id, owner_id, created_at, updated_at
            """,
            content,
            task_id,
            owner_id,
        )
        return dict(record) if record is not None else None

    async def list_comments_by_task(self, task_id: int) -> List[Dict[str, Any]]:
        records = await self.fetch_all(
            """
            SELECT id, content, task_id, owner_id, created_at, updated_at
            FROM comments.comment
            WHERE task_id = $1
            ORDER BY created_at ASC
            """,
            task_id,
        )
        return [dict(r) for r in records]

    async def delete_comment(self, comment_id: int, owner_id: int) -> bool:
        result = await self.execute(
            "DELETE FROM comments.comment WHERE id = $1 AND owner_id = $2",
            comment_id,
            owner_id,
        )
        return result == "DELETE 1"