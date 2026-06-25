from shared.exceptions.base import AppException

class UserServiceError(AppException):
    pass


class UserNotFound(AppException):
    status_code = 404
    error_code = "USER_NOT_FOUND"
    default_message = "User not found"


class EmailAlreadyTaken(AppException):
    status_code = 409
    error_code = "USER_EMAIL_TAKEN"
    default_message = "This email is already in use"