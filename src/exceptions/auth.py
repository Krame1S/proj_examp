from fastapi import status

from .base import AppException


class InvalidCredentials(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "AUTH_INVALID_CREDENTIALS"
    default_message = "Invalid email or password"


class EmailAlreadyRegistered(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "AUTH_EMAIL_ALREADY_REGISTERED"
    default_message = "Email is already registered"


class InvalidRefreshToken(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "AUTH_INVALID_REFRESH_TOKEN"
    default_message = "Invalid or expired refresh token"


class AccountDeactivated(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "AUTH_ACCOUNT_DEACTIVATED"
    default_message = "Account is deactivated"