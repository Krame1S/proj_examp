import jwt
from fastapi import HTTPException, status
from src.core.config import settings

_public_key: str | None = None


def load_public_key(path: str) -> None:
    global _public_key
    try:
        with open(path) as f:
            _public_key = f.read()
    except Exception as e:
        raise RuntimeError("Failed to load JWT public key") from e


def decode_access_token(token: str) -> int:
    if _public_key is None:
        raise RuntimeError("JWT public key not loaded")
    try:
        payload = jwt.decode(token, _public_key, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired") from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from e
    if payload.get("type") != "access":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type")
    return int(payload["sub"])