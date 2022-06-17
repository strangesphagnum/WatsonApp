import logging
from datetime import datetime, timezone

from typing import Optional

from aiogram.types import Message

from models import User
from application.serializers import MessageDataSerializer
from application.repositories import UserRepository
from application.exceptions import TooManyAttemptsError
from settings import settings


""" TODO:
set interaction with rabbitmq
"""


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository: UserRepository = user_repository

    async def _get_user(self, message: Message) -> Optional[User]:
        """TODO: get rid of inner method
        in order not to generate redundancy"""
        user_data = MessageDataSerializer.parse_user_data(message=message)
        return await self._user_repository.get_record(
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
        await self._user_repository.update_record_last_uploaded(user.telegram_user_id)

    async def create_user_if_none(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        user = await self._get_user(message)
        if user is None:
            await self._user_repository.create_record(
                telegram_user_id=user_data.telegram_user_id,
                telegram_chat_id=user_data.telegram_chat_id,
            )
