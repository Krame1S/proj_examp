from fastapi import status

from src.exceptions.base import AppException


class TagNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "TAG_NOT_FOUND"
    default_message = "Tag not found"


class TagAlreadyExists(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "TAG_ALREADY_EXISTS"
    default_message = "Tag with this name already exists"