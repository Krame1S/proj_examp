from enum import Enum


class ConsumerQueue(Enum):
    # User service
    AUTH_SIGN_UP = "auth.sign_up"
    AUTH_SIGN_IN = "auth.sign_in"
    AUTH_REFRESH = "auth.refresh"
    USER_GET_PROFILE = "user.get_profile"
    USER_UPDATE_PROFILE = "user.update_profile"
    USER_DELETE = "user.delete"

    # Task service
    TASK_CREATE = "task.create"
    TASK_LIST = "task.list"
    TASK_GET_BY_ID = "task.get_by_id"
    TASK_PATCH = "task.patch"
    TASK_DELETE = "task.delete"

    # Category service
    CATEGORY_CREATE = "category.create"
    CATEGORY_LIST = "category.list"
    CATEGORY_GET_BY_ID = "category.get_by_id"
    CATEGORY_PATCH = "category.patch"
    CATEGORY_DELETE = "category.delete"

    # Tag service
    TAG_CREATE = "tag.create"
    TAG_LIST = "tag.list"
    TAG_GET_BY_ID = "tag.get_by_id"
    TAG_PATCH = "tag.patch"
    TAG_DELETE = "tag.delete"

    # Comment service
    COMMENT_CREATE = "comment.create"
    COMMENT_LIST = "comment.list"
    COMMENT_DELETE = "comment.delete"

    # Attachment service
    ATTACHMENT_CREATE = "attachment.create"
    ATTACHMENT_LIST = "attachment.list"
    ATTACHMENT_DELETE = "attachment.delete"

    # Chat service
    CHAT_REQUEST_CREATE = "chat.request.create"
    CHAT_REQUEST_LIST = "chat.request.list"
    CHAT_REQUEST_CANCEL = "chat.request.cancel"
    CHAT_REQUEST_ACCEPT = "chat.request.accept"
    CHAT_REQUEST_DECLINE = "chat.request.decline"
    CHAT_ROOM_LIST = "chat.room.list"
    CHAT_ROOM_GET = "chat.room.get"
    CHAT_MESSAGE_CREATE = "chat.message.create"
    CHAT_MESSAGE_LIST = "chat.message.list"


class ResponseQueue(Enum):
    DEFAULT = "rpc_response"
