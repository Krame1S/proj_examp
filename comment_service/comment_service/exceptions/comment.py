from .base import AppException

class CommentNotFound(AppException):
    status_code = 404
    error_code = "COMMENT_NOT_FOUND"
    default_message = "Comment not found"