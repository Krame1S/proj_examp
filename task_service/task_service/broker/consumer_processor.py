import json
import logging

from shared.contracts.task.contracts import TaskIn, TaskListRequest, TaskUpdate
from shared.exceptions.base import AppException

from task_service.services.task import TaskService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_task(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = TaskIn(**data)
            service = await TaskService.create()
            result = await service.create_task(request, owner_id=data["user_id"])
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_task")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_tasks(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = TaskListRequest(**data)
            service = await TaskService.create()
            result = await service.list_tasks(
                owner_id=request.user_id,
                limit=request.limit,
                category_id=request.category_id,
                tag_ids=request.tag_ids,
                status_filter=request.status_filter,
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_tasks")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def get_task_by_id(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await TaskService.create()
            result = await service.get_task_by_id(
                owner_id=data["user_id"],
                task_id=data["task_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in get_task_by_id")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def patch_task(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = TaskUpdate(**data)
            service = await TaskService.create()
            result = await service.patch_task(
                task_id=data["task_id"],
                update_data=request,
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in patch_task")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def delete_task(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await TaskService.create()
            await service.delete_task(
                task_id=data["task_id"],
                user_id=data["user_id"],
            )
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_task")
            return json.dumps(AppException().to_dict())
