from shared.exceptions.base import AppException


class CommentServiceError(AppException):
    pass


class CommentNotFound(AppException):
    status_code = 404
    error_code = "COMMENT_NOT_FOUND"
    default_message = "Comment not found"
