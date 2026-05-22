class AuthServiceError(Exception):
    pass

class EmailAlreadyRegistered(AuthServiceError):
    pass

class InvalidCredentials(AuthServiceError):
    pass

class AccountDeactivated(AuthServiceError):
    pass

class InvalidRefreshToken(AuthServiceError):
    pass

class TokenExpired(AuthServiceError):
    pass

class InvalidToken(AuthServiceError):
    pass