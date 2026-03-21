from fastapi import status

from .base import AppException


class UserNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "USER_NOT_FOUND"
    default_message = "User not found"