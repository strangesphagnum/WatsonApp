import logging
from datetime import datetime

from aiogram.types import Message

from application.serializers import MessageDataSerializer
from application.repositories import UserRepository
from application.exceptions import TooManyAttemptsError


""" TODO:
1. Set interaction with rabbitmq
"""


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository: UserRepository = user_repository

    async def update_user_uploaded_date(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        user = await self._user_repository.get_record(
            telegram_user_id=user_data.telegram_user_id
        )
        now = datetime.now()
        if (user.last_uploaded is not None) and ((now - user.last_uploaded).days < 1):
            raise TooManyAttemptsError
        await self._user_repository.update_record_last_uploaded(user.telegram_user_id)

    async def create_user_if_none(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        user = await self._user_repository.get_record(
            telegram_user_id=user_data.telegram_user_id
        )
        if user is None:
            await self._user_repository.create_record(
                telegram_user_id=user_data.telegram_user_id,
                telegram_chat_id=user_data.telegram_chat_id,
            )
