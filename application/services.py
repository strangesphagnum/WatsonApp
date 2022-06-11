import logging
from datetime import datetime, timezone

from typing import Optional

from aiogram.types import Message

from models import User
from application.serializers import UserData, MessageDataSerializer
from application.repositories import HandlersRepository
from application.exceptions import TooManyAttemptsError
from settings import settings


class HandlersService:
    def __init__(self, handlers_repository):
        logging.info("HandlersService initialized")
        self._handlers_repository: HandlersRepository = handlers_repository

    async def _get_user(self, message: Message) -> Optional[User]:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        return await self._handlers_repository.get_user(
            telegram_user_id=user_data.telegram_user_id
        )

    async def update_user_uploaded_date(self, message: Message) -> None:
        # TODO: simplify dt calc, check for last_uploaded data type
        user = await self._get_user(message)
        now = datetime.now(timezone.utc)
        if (user.last_uploaded is not None) and (
            (now - user.last_uploaded).total_seconds() < settings.SECONDS_PER_DAY
        ):
            raise TooManyAttemptsError
        await self._handlers_repository.update_user_last_uploaded(user.telegram_user_id)

    async def create_user_if_none(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        user = await self._get_user(message)
        if user is None:
            await self._handlers_repository.create_user(
                telegram_user_id=user_data.telegram_user_id,
                telegram_chat_id=user_data.telegram_chat_id,
            )
