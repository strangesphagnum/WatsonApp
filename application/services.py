import logging
from datetime import datetime

from aiogram.types import Message

from application.serializers import MessageDataSerializer
from application.repositories import UserRepository, RabbitRepository
from application.exceptions import TooManyAttemptsError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository: UserRepository = user_repository

    async def check_uploaded_date(self, message: Message) -> None:
        message_data = MessageDataSerializer.parse_message_data(message=message)
        user = await self._user_repository.get_record(
            telegram_user_id=message_data.telegram_user_id
        )
        now = datetime.now()
        if (user.last_uploaded is not None) and ((now - user.last_uploaded).days < 1):
            raise TooManyAttemptsError

    async def update_uploaded_date(self, message: Message) -> None:
        message_data = MessageDataSerializer.parse_message_data(message=message)
        user = await self._user_repository.get_record(
            telegram_user_id=message_data.telegram_user_id
        )
        await self._user_repository.update_record_last_uploaded(user.telegram_user_id)

    async def create_if_none(self, message: Message) -> None:
        message_data = MessageDataSerializer.parse_message_data(message=message)
        user = await self._user_repository.get_record(
            telegram_user_id=message_data.telegram_user_id
        )
        if user is None:
            await self._user_repository.create_record(
                telegram_user_id=message_data.telegram_user_id,
                telegram_chat_id=message_data.telegram_chat_id,
            )


class UserRabbitService:
    def __init__(self, rabbit_repository: RabbitRepository):
        self._rabbit_repository: RabbitRepository = rabbit_repository

    async def publish_message(self, message: Message) -> None:
        message_data = MessageDataSerializer.parse_message_data(message=message)
        message = f"{message_data.telegram_chat_id}:{message_data.document_id}"
        await self._rabbit_repository.publish_record(message=message)
