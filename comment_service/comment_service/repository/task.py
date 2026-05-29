from typing import Any, Dict, Optional
from comment_service.repository.base import BaseRepository


class TaskRepository(BaseRepository):

    async def get_task_by_id(self, task_id: int, owner_id: int) -> Optional[Dict[str, Any]]:
        record = await self.fetch_row(
            """
            SELECT id FROM tasks.task
            WHERE id = $1 AND owner_id = $2
            """,
            task_id,
            owner_id,
        )
        return dict(record) if record is not None else None