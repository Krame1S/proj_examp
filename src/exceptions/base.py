from dataclasses import dataclass
from typing import Any, Dict, Optional

from fastapi import status


@dataclass
class ErrorPayload:
    code: str
    message: str
    detail: Optional[Any] = None
    request_id: Optional[str] = None


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
        message: Optional[str] = None,
        detail: Optional[Any] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
    ):
        self.message = message or self.default_message
        self.detail = detail
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code

    def to_dict(self, request_id: Optional[str] = None) -> Dict[str, Any]:
        payload = ErrorPayload(
            code=self.error_code,
            message=self.message,
            detail=self.detail,
            request_id=request_id,
        )
        return {"error": payload.__dict__}