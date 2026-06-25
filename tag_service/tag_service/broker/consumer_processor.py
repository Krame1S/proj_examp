import json
import logging

from shared.contracts.tag.contracts import TagCreate, TagUpdate
from shared.exceptions.base import AppException

from tag_service.services.tag import TagService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_tag(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = TagCreate(**data)
            service = await TagService.create()
            result = await service.create_tag(request, user_id=data["user_id"])
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_tag")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_tags(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await TagService.create()
            results = await service.list_by_user(user_id=data["user_id"])
            return json.dumps([r.model_dump() for r in results])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_tags")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def get_tag_by_id(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await TagService.create()
            result = await service.get_tag_by_id(tag_id=data["tag_id"], user_id=data["user_id"])
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in get_tag_by_id")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def patch_tag(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = TagUpdate(**data)
            service = await TagService.create()
            result = await service.update_tag(
                tag_id=data["tag_id"],
                tag_update=request,
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in patch_tag")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def delete_tag(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await TagService.create()
            await service.delete_tag(tag_id=data["tag_id"], user_id=data["user_id"])
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_tag")
            return json.dumps(AppException().to_dict())
