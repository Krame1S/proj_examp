from shared.exceptions.base import AppException


class TagServiceError(AppException):
    pass


class TagNotFound(TagServiceError):
    status_code = 404
    error_code = "TAG_NOT_FOUND"
    default_message = "Tag not found"