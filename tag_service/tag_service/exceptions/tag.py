from shared.exceptions.base import AppException

class TagServiceError(AppException):
    pass

class TagNotFound(AppException):
    status_code = 404
    error_code = "TAG_NOT_FOUND"
    default_message = "Tag not found"


class TagAlreadyExists(AppException):
    status_code = 409
    error_code = "TAG_ALREADY_EXISTS"
    default_message = "Tag with this name already exists"