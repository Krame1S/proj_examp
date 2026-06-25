import json
import logging

from shared.contracts.category.contracts import (
    CategoryCreate,
    CategoryListRequest,
    CategoryUpdate,
)
from shared.exceptions.base import AppException

from category_service.services.category import CategoryService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_category(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = CategoryCreate(**data)
            service = await CategoryService.create()
            result = await service.create_category(
                request=request,
                owner_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_category")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_categories(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = CategoryListRequest(**data)
            service = await CategoryService.create()
            result = await service.list_categories(
                owner_id=request.user_id,
                limit=request.limit,
                parent_id=getattr(request, "parent_id", None),
            )
            return json.dumps([r.model_dump() for r in result])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_categories")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def get_category_by_id(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await CategoryService.create()
            result = await service.get_category_by_id(
                owner_id=data["user_id"],
                category_id=data["category_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in get_category_by_id")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def patch_category(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = CategoryUpdate(**data)
            service = await CategoryService.create()
            result = await service.patch_category(
                category_id=data["category_id"],
                update_data=request,
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in patch_category")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def delete_category(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await CategoryService.create()
            await service.delete_category(
                category_id=data["category_id"],
                user_id=data["user_id"],
            )
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_category")
            return json.dumps(AppException().to_dict())
