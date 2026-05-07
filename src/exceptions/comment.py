from fastapi import status
from src.exceptions.base import AppException


class CommentNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "COMMENT_NOT_FOUND"
    default_message = "Comment not found"