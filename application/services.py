import logging

from models import User
from application.serializers import UserData, MessageDataSerializer
from aiogram.types import Message

from application.repositories import HandlersRepository


class HandlersService:
    def __init__(self, handlers_repository):
        logging.info("HandlersService initialized")
        self.handlers_repository: HandlersRepository = handlers_repository

    async def create_user(self, message: Message) -> None:
        user_data = MessageDataSerializer.parse_user_data(message=message)
        await self.handlers_repository.create_user(user_data=user_data)
