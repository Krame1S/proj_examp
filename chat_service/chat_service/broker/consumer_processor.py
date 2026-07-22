import json
import logging

from shared.exceptions.base import AppException

from chat_service.services.chat import ChatService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def create_request(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.create_request(
                requester_id=data["user_id"],
                email=data["email"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_request")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_requests(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            results = await service.list_requests(
                user_id=data["user_id"],
                direction=data["direction"],
                status=data.get("status"),
            )
            return json.dumps([r.model_dump() for r in results])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_requests")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def accept_request(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.accept_request(
                request_id=data["request_id"],
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in accept_request")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def decline_request(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.decline_request(
                request_id=data["request_id"],
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in decline_request")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def cancel_request(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.cancel_request(
                request_id=data["request_id"],
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in cancel_request")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_rooms(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            results = await service.list_rooms(user_id=data["user_id"])
            return json.dumps([r.model_dump() for r in results])
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_rooms")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def get_room(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.get_room(
                room_id=data["room_id"],
                user_id=data["user_id"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in get_room")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def create_message(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.create_message(
                room_id=data["room_id"],
                sender_id=data["user_id"],
                content=data["content"],
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in create_message")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def list_messages(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await ChatService.create()
            result = await service.list_messages(
                room_id=data["room_id"],
                user_id=data["user_id"],
                limit=data.get("limit", 20),
                before_id=data.get("before_id"),
            )
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in list_messages")
            return json.dumps(AppException().to_dict())
