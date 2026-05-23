from enum import Enum


class ConsumerQueue(Enum):
    AUTH_SIGN_UP = "auth.sign_up"
    AUTH_SIGN_IN = "auth.sign_in"
    AUTH_REFRESH = "auth.refresh"
    USER_GET_PROFILE = "user.get_profile"
    USER_UPDATE_PROFILE = "user.update_profile"
    USER_DELETE = "user.delete"


class ResponseQueue(Enum):
    DEFAULT = "rpc_response"