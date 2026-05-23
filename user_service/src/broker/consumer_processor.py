import json
import logging

from src.exceptions.auth import AuthServiceError, EmailAlreadyRegistered
from src.exceptions.base import AppException
from src.schemas.auth import RefreshRequest, SignInRequest, SignUpRequest
from src.services.auth import AuthService

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