from src.exceptions.comment import CommentNotFound
from src.exceptions.task import TaskNotFound
from src.repository.comment import CommentRepository
from src.repository.task import TaskRepository
from src.schemas.comment import CommentIn, CommentOut


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository,
        task_repository: TaskRepository,
    ):
        self.comment_repository = comment_repository
        self.task_repository = task_repository

    async def create_comment(
        self,
        task_id: int,
        owner_id: int,
        comment_in: CommentIn,
    ) -> CommentOut:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()

        record = await self.comment_repository.create_comment(
            content=comment_in.content,
            task_id=task_id,
            owner_id=owner_id,
        )
        if record is None:
            raise RuntimeError("Comment creation failed")

        return CommentOut.from_db_row(record)

    async def list_comments(
        self,
        task_id: int,
        owner_id: int,
    ) -> list[CommentOut]:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()

        records = await self.comment_repository.list_comments_by_task(task_id)
        return [CommentOut.from_db_row(r) for r in records]

    async def delete_comment(
        self,
        comment_id: int,
        owner_id: int,
    ) -> None:
        deleted = await self.comment_repository.delete_comment(comment_id, owner_id)
        if not deleted:
            raise CommentNotFound()