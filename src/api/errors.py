import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.exceptions.base import AppException

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        logger.warning(
            "%s - %s",
            exc.error_code,
            exc.message,
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "detail": exc.detail,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "Unhandled exception occurred",
            extra={"request_id": request_id},
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "detail": None,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError | ValidationError
    ):
        logger.info(
            "Request validation failed",
            extra={"errors": exc.errors(), "request_id": getattr(request.state, "request_id", None)},
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "detail": exc.errors(),
                }
            },
        )