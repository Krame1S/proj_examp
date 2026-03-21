from dataclasses import dataclass
from typing import Any, Dict

from fastapi import status


@dataclass
class ErrorPayload:
    code: str
    message: str
    detail: Any | None = None


class AppException(Exception):
    """
    Base class for all application-level (business) exceptions.
    All expected/handled errors should inherit from this class.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_SERVER_ERROR"
    default_message: str = "Internal server error"

    def __init__(
        self,
        message: str | None = None,
        detail: Any | None = None,
        status_code: int | None = None,
        error_code: str | None = None,
    ):
        self.message = message or self.default_message
        self.detail = detail
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code

    def to_dict(self) -> Dict[str, Any]:
        payload = ErrorPayload(
            code=self.error_code,
            message=self.message,
            detail=self.detail,
        )
        return {"error": payload.__dict__}