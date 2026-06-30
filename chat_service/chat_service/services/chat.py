from shared.contracts.chats.contracts import ChatRequestOut, GetMessagesResponse, MessageOut

from chat_service.core.database import get_db_pool
from chat_service.exceptions.chat import (
    ChatRequestAlreadyExists,
    ChatRequestNotFound,
    Forbidden,
    SelfRequest,
    UserNotFound,
)
from chat_service.repository.chat_message import ChatMessageRepository
from chat_service.repository.chat_request import ChatRequestRepository
from chat_service.repository.user import UserRepository


class ChatService:
    def __init__(
        self,
        chat_request_repository: ChatRequestRepository,
        chat_message_repository: ChatMessageRepository,
        user_repository: UserRepository,
    ):
        self.chat_request_repo = chat_request_repository
        self.chat_message_repo = chat_message_repository
        self.user_repo = user_repository

    @classmethod
    async def create(cls) -> "ChatService":
        pool = await get_db_pool()
        return cls(
            chat_request_repository=ChatRequestRepository(pool),
            chat_message_repository=ChatMessageRepository(pool),
            user_repository=UserRepository(pool),
        )

    async def create_request(self, requester_id: int, email: str) -> ChatRequestOut:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            raise UserNotFound
        if user["id"] == requester_id:
            raise SelfRequest
        existing = await self.chat_request_repo.get_active_between(requester_id, user["id"])
        if existing is not None:
            raise ChatRequestAlreadyExists
        record = await self.chat_request_repo.create(requester_id, user["id"])
        if record is None:
            raise RuntimeError("Failed to create chat request")
        return ChatRequestOut.from_db_row(record)

    async def list_requests(self, user_id: int, direction: str, status: str | None = None) -> list[ChatRequestOut]:
        records = await self.chat_request_repo.list_by_user(user_id, direction, status)
        return [ChatRequestOut.from_db_row(r) for r in records]

    async def accept_request(self, request_id: int, user_id: int) -> ChatRequestOut:
        request = await self.chat_request_repo.get_by_id(request_id)
        if request is None or request["target_id"] != user_id:
            raise ChatRequestNotFound
        if request["status"] != "pending":
            raise ChatRequestNotFound
        record = await self.chat_request_repo.update_status(request_id, "accepted")
        if record is None:
            raise RuntimeError("Failed to update request status")
        return ChatRequestOut.from_db_row(record)

    async def decline_request(self, request_id: int, user_id: int) -> ChatRequestOut:
        request = await self.chat_request_repo.get_by_id(request_id)
        if request is None or request["target_id"] != user_id:
            raise ChatRequestNotFound
        if request["status"] != "pending":
            raise ChatRequestNotFound
        record = await self.chat_request_repo.update_status(request_id, "declined")
        if record is None:
            raise RuntimeError("Failed to update request status")
        return ChatRequestOut.from_db_row(record)

    async def cancel_request(self, request_id: int, user_id: int) -> ChatRequestOut:
        request = await self.chat_request_repo.get_by_id(request_id)
        if request is None or request["requester_id"] != user_id:
            raise ChatRequestNotFound
        if request["status"] != "pending":
            raise ChatRequestNotFound
        record = await self.chat_request_repo.update_status(request_id, "cancelled")
        if record is None:
            raise RuntimeError("Failed to update request status")
        return ChatRequestOut.from_db_row(record)

    async def get_room(self, room_id: int, user_id: int) -> ChatRequestOut:
        request = await self.chat_request_repo.get_by_id(room_id)
        if request is None:
            raise ChatRequestNotFound
        if request["requester_id"] != user_id and request["target_id"] != user_id:
            raise Forbidden
        return ChatRequestOut.from_db_row(request)

    async def create_message(self, room_id: int, sender_id: int, content: str) -> MessageOut:
        record = await self.chat_message_repo.create(room_id, sender_id, content)
        if record is None:
            raise RuntimeError("Failed to create message")
        return MessageOut.from_db_row(record)

    async def list_messages(self, room_id: int, user_id: int, limit: int, before_id: int | None) -> GetMessagesResponse:
        room = await self.chat_request_repo.get_by_id(room_id)
        if room is None:
            raise ChatRequestNotFound
        if room["requester_id"] != user_id and room["target_id"] != user_id:
            raise Forbidden
        records = await self.chat_message_repo.list_by_room(room_id, limit + 1, before_id)
        has_more = len(records) > limit
        return GetMessagesResponse(
            messages=[MessageOut.from_db_row(r) for r in records[:limit]],
            has_more=has_more,
        )

    async def list_rooms(self, user_id: int) -> list[ChatRequestOut]:
        records = await self.chat_request_repo.list_accepted_by_user(user_id)
        return [ChatRequestOut.from_db_row(r) for r in records]
