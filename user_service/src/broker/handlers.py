import json
import logging

from src.exceptions.auth import EmailAlreadyRegistered
from src.schemas.auth import SignUpRequest
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
        except EmailAlreadyRegistered:
            return json.dumps({"error": "EMAIL_ALREADY_REGISTERED"})
        except Exception as e:
            logger.exception("Unexpected error in sign_up")
            return json.dumps({"error": "INTERNAL_ERROR"})