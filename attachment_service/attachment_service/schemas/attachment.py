from shared.contracts.attachment.contracts import AttachmentOut as AttachmentOutBase


class AttachmentOut(AttachmentOutBase):
    @classmethod
    def from_db_row(cls, row: dict) -> "AttachmentOut":
        from attachment_service.utils.s3 import get_public_url
        return cls(
            id=row["id"],
            task_id=row["task_id"],
            owner_id=row["owner_id"],
            filename=row["filename"],
            content_type=row["content_type"],
            size=row["size"],
            url=get_public_url(row["key"]),
            created_at=row["created_at"].isoformat() if row.get("created_at") else None,
        )