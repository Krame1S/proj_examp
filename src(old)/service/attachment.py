import uuid

from src.exceptions.attachment import AttachmentNotFound, AttachmentUploadFailed
from src.exceptions.task import TaskNotFound
from src.repository.attachment import AttachmentRepository
from src.repository.task import TaskRepository
from src.schemas.attachment import AttachmentOut
from src.utils.s3 import delete_object, upload_bytes


class AttachmentService:
    def __init__(
        self,
        attachment_repository: AttachmentRepository,
        task_repository: TaskRepository,
    ):
        self.attachment_repository = attachment_repository
        self.task_repository = task_repository

    async def upload_attachment(
        self,
        task_id: int,
        owner_id: int,
        filename: str,
        content_type: str,
        data: bytes,
    ) -> AttachmentOut:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()

        # генерируем уникальный key для S3
        extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
        key = f"attachments/task_{task_id}/{uuid.uuid4().hex}"
        if extension:
            key = f"{key}.{extension}"

        try:
            await upload_bytes(key=key, data=data, content_type=content_type)
        except Exception:
            raise AttachmentUploadFailed()

        record = await self.attachment_repository.create_attachment(
            task_id=task_id,
            owner_id=owner_id,
            key=key,
            filename=filename,
            content_type=content_type,
            size=len(data),
        )
        if record is None:
            raise RuntimeError("Attachment creation failed")

        return AttachmentOut.from_db_row(record)

    async def list_attachments(
        self,
        task_id: int,
        owner_id: int,
    ) -> list[AttachmentOut]:
        task = await self.task_repository.get_task_by_id(task_id, owner_id)
        if task is None:
            raise TaskNotFound()

        records = await self.attachment_repository.list_attachments_by_task(task_id)
        return [AttachmentOut.from_db_row(r) for r in records]

    async def delete_attachment(
        self,
        attachment_id: int,
        owner_id: int,
    ) -> None:
        record = await self.attachment_repository.get_attachment_by_id(attachment_id)
        if record is None or record["owner_id"] != owner_id:
            raise AttachmentNotFound()

        try:
            await delete_object(record["key"])
        except Exception:
            pass 

        deleted = await self.attachment_repository.delete_attachment(attachment_id, owner_id)
        if not deleted:
            raise AttachmentNotFound()