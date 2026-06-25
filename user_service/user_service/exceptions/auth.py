from shared.exceptions.base import AppException

class AuthServiceError(AppException):
    pass


class EmailAlreadyRegistered(AuthServiceError):
    status_code = 409
    error_code = "EMAIL_ALREADY_REGISTERED"
    default_message = "Email already registered"


class InvalidCredentials(AuthServiceError):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"
    default_message = "Invalid email or password"


class AccountDeactivated(AuthServiceError):
    status_code = 403
    error_code = "ACCOUNT_DEACTIVATED"
    default_message = "Account is deactivated"


class InvalidRefreshToken(AuthServiceError):
    status_code = 401
    error_code = "INVALID_REFRESH_TOKEN"
    default_message = "Refresh token is invalid or expired"


class TokenExpired(AuthServiceError):
    status_code = 401
    error_code = "TOKEN_EXPIRED"
    default_message = "Token has expired"


class InvalidToken(AuthServiceError):
    status_code = 401
    error_code = "INVALID_TOKEN"
    default_message = "Token is invalid"