from shared.exceptions.base import AppException


class AuthServiceError(AppException):
    pass


class EmailAlreadyRegisteredError(AuthServiceError):
    status_code = 409
    error_code = "EMAIL_ALREADY_REGISTERED"
    default_message = "Email already registered"


class InvalidCredentialsError(AuthServiceError):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"
    default_message = "Invalid email or password"


class AccountDeactivatedError(AuthServiceError):
    status_code = 403
    error_code = "ACCOUNT_DEACTIVATED"
    default_message = "Account is deactivated"


class InvalidRefreshTokenError(AuthServiceError):
    status_code = 401
    error_code = "INVALID_REFRESH_TOKEN"
    default_message = "Refresh token is invalid or expired"


class TokenExpiredError(AuthServiceError):
    status_code = 401
    error_code = "TOKEN_EXPIRED"
    default_message = "Token has expired"


class InvalidTokenErrorError(AuthServiceError):
    status_code = 401
    error_code = "INVALID_TOKEN"
    default_message = "Token is invalid"
