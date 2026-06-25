import contextlib

from attachment_service.core.database import get_db_pool
from attachment_service.exceptions.attachment import AttachmentNotFound
from attachment_service.exceptions.task import TaskNotFoundError
from attachment_service.repository.attachment import AttachmentRepository
from attachment_service.repository.task import TaskRepository
from attachment_service.schemas.attachment import AttachmentOut
from attachment_service.utils.s3 import delete_object


class AttachmentService:
    def __init__(
        self,
        attachment_repository: AttachmentRepository,
        task_repository: TaskRepository,
    ):
        self.attachment_repository = attachment_repository
        self.task_repository = task_repository

    @classmethod
    async def create(cls) -> "AttachmentService":
        pool = await get_db_pool()
        return cls(
            attachment_repository=AttachmentRepository(pool),
            task_repository=TaskRepository(pool),
        )

    async def create_attachment(
        self,
        task_id: int,
        owner_id: int,
        key: str,
        filename: str,
        content_type: str,
        size: int,
    ) -> AttachmentOut:
        """Persist attachment metadata.

        The file is already in S3 — the gateway uploaded it before calling us.
        We only validate task ownership and write the DB row.
        """
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFoundError

        record = await self.attachment_repository.create_attachment(
            task_id=task_id,
            owner_id=owner_id,
            key=key,
            filename=filename,
            content_type=content_type,
            size=size,
        )
        if record is None:
            raise RuntimeError("Attachment creation failed")

        return AttachmentOut.from_db_row(record)

    async def list_attachments(self, task_id: int, owner_id: int) -> list[AttachmentOut]:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFoundError

        records = await self.attachment_repository.list_attachments_by_task(task_id)
        return [AttachmentOut.from_db_row(r) for r in records]

    async def delete_attachment(self, attachment_id: int, owner_id: int) -> None:
        record = await self.attachment_repository.get_by_id(attachment_id)
        if record is None or record["owner_id"] != owner_id:
            raise AttachmentNotFound

        # Best-effort S3 cleanup — don't fail the request if S3 is unavailable
        with contextlib.suppress(Exception):
            await delete_object(record["key"])

        deleted = await self.attachment_repository.delete_attachment(attachment_id, owner_id)
        if not deleted:
            raise AttachmentNotFound
