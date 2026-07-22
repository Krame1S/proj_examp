import json
import logging

from shared.exceptions.base import AppException

from attachment_service.services.attachment import AttachmentService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_attachment(message: bytes) -> str:
        """Persist attachment metadata after the gateway has uploaded the file to S3."""
        try:
            data = json.loads(message)
            service = await AttachmentService.create()
            result = await service.create_attachment(
                task_id=data["task_id"],
                owner_id=data["owner_id"],
                key=data["key"],
                filename=data["filename"],
                content_type=data["content_type"],
                size=data["size"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_attachment")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_attachments(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await AttachmentService.create()
            results = await service.list_attachments(
                task_id=data["task_id"],
                owner_id=data["owner_id"],
            )
            return json.dumps([r.model_dump() for r in results])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_attachments")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def delete_attachment(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await AttachmentService.create()
            await service.delete_attachment(
                attachment_id=data["attachment_id"],
                owner_id=data["owner_id"],
            )
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_attachment")
            return json.dumps(AppException().to_dict())
