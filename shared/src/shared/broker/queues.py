from enum import Enum


class ConsumerQueue(Enum):
    AUTH_SIGN_UP = "auth.sign_up"
    AUTH_SIGN_IN = "auth.sign_in"
    AUTH_REFRESH = "auth.refresh"
    USER_GET = "user.get"
    USER_UPDATE = "user.update"


class ResponseQueue(Enum):
    DEFAULT = "rpc_response"