from typing import Optional

from pydantic import BaseModel
from aiogram.types import Message


class UserData(BaseModel):
    telegram_user_id: int
    telegram_chat_id: int
    document_id: Optional[str]


class MessageDataSerializer:
    @classmethod
    def parse_message_data(cls, message: Message) -> UserData:
        message = dict(message)
        document = message.get("document")
        return UserData(
            telegram_user_id=message.get("from").get("id"),
            telegram_chat_id=message.get("chat").get("id"),
            document_id=document.get("file_id") if document else None,
        )
