import json
import logging

from comment_service.exceptions.base import AppException
from comment_service.schemas.comment import CommentIn
from comment_service.services.comment import CommentService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_comment(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = CommentIn(**data)
            service = await CommentService.create()
            result = await service.create_comment(
                task_id=data["task_id"],
                owner_id=data["user_id"],
                comment_in=request,
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_comment")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_comments(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await CommentService.create()
            results = await service.list_comments(
                task_id=data["task_id"],
                owner_id=data["user_id"],
            )
            return json.dumps([r.model_dump() for r in results])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_comments")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def delete_comment(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await CommentService.create()
            await service.delete_comment(
                comment_id=data["comment_id"],
                owner_id=data["user_id"],
            )
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_comment")
            return json.dumps(AppException().to_dict())