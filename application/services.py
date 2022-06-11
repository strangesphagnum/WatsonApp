import logging

from models import User
from application.serializers import UserData, MessageDataSerializer
from aiogram.types import Message

from application.repositories import HandlersRepository


class HandlersService:
    def __init__(self, handlers_repository):
        logging.info("HandlersService initialized")
        self._handlers_repository: HandlersRepository = handlers_repository

    async def create_user_if_none(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        user = await self._handlers_repository.get_user(
            telegram_user_id=user_data.telegram_user_id
        )
        if user is None:
            await self._handlers_repository.create_user(
                telegram_user_id=user_data.telegram_user_id,
                telegram_chat_id=user_data.telegram_chat_id,
            )
