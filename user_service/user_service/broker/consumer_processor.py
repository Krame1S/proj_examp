import json
import logging

from user_service.exceptions.auth import AuthServiceError, EmailAlreadyRegistered
from user_service.exceptions.base import AppException
from user_service.schemas.auth import RefreshRequest, SignInRequest, SignUpRequest
from user_service.services.auth import AuthService
from user_service.services.user import UserService

logger = logging.getLogger(__name__)


class ConsumerProcessor:
    @staticmethod
    async def sign_up(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = SignUpRequest(**data)
            service = await AuthService.create()
            result = await service.sign_up(request)
            return result.model_dump_json()
        except AuthServiceError as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in sign_up")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def sign_in(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = SignInRequest(**data)
            service = await AuthService.create()
            result = await service.sign_in(request)
            return result.model_dump_json()
        except AuthServiceError as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in sign_in")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def refresh(message: bytes) -> str:
        try:
            data = json.loads(message)
            request = RefreshRequest(**data)
            service = await AuthService.create()
            result = await service.refresh(request.refresh_token)
            return result.model_dump_json()
        except AuthServiceError as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in refresh")
            return json.dumps(AppException().to_dict())

    @staticmethod
    async def get_profile(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await UserService.create()
            result = await service.get_profile(data["user_id"])
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in get_profile")
            return json.dumps(AppException().to_dict())


    @staticmethod
    async def update_profile(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await UserService.create()
            result = await service.update_email(data["user_id"], data.get("email"))
            return result.model_dump_json()
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in update_profile")
            return json.dumps(AppException().to_dict())


    @staticmethod
    async def delete_account(message: bytes) -> str:
        try:
            data = json.loads(message)
            service = await UserService.create()
            await service.delete(data["user_id"])
            return json.dumps({})
        except AppException as e:
            return json.dumps(e.to_dict())
        except Exception:
            logger.exception("Unexpected error in delete_account")
            return json.dumps(AppException().to_dict())