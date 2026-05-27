from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ErrorPayload:
    code: str
    message: str
    status_code: int
    detail: Optional[Any] = None


class AppException(Exception):
    status_code: int = 500
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

    def to_dict(self) -> dict:
        payload = ErrorPayload(
            code=self.error_code,
            message=self.message,
            status_code=self.status_code,
            detail=self.detail,
        )
        return {"error": payload.__dict__}