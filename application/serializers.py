from pydantic import BaseModel
from aiogram.types import Message


class UserData(BaseModel):
    telegram_user_id: int
    telegram_chat_id: int


class MessageDataSerializer:
    @classmethod
    def parse_user_data(cls, message: Message) -> UserData:
        return UserData(
            telegram_user_id = message["from"]["id"],
            telegram_chat_id = message["chat"]["id"]
        )
