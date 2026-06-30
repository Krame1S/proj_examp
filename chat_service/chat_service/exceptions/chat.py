from shared.exceptions.base import AppException


class UserNotFound(AppException):
    status_code = 404
    error_code = "USER_NOT_FOUND"
    default_message = "User not found"


class SelfRequest(AppException):
    status_code = 400
    error_code = "SELF_REQUEST"
    default_message = "Cannot send chat request to yourself"


class ChatRequestAlreadyExists(AppException):
    status_code = 409
    error_code = "ALREADY_EXISTS"
    default_message = "Chat request already exists"


class ChatRequestNotFound(AppException):
    status_code = 404
    error_code = "CHAT_REQUEST_NOT_FOUND"
    default_message = "Chat request not found"


class Forbidden(AppException):
    status_code = 403
    error_code = "FORBIDDEN"
    default_message = "You don't have permission to perform this action"
