from aiogram.types import Message, ContentTypes

from application.dispatcher import dispatcher
from application.messages import (
    WELCOME,
    TYPE_ERROR,
    FILE_IN_PROCESS
)
from models import User
from application.serializers import MessageDataSerializer


@dispatcher.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    user_data = MessageDataSerializer.parse_user_data(message=message)
    user = User(
        telegram_user_id=user_data.telegram_user_id,
        telegram_chat_id=user_data.telegram_chat_id
    )
    db_session = message.bot.get("db")

    async with db_session() as session:
        session.add(user)
        await session.commit()
    await message.reply(WELCOME)


# The order is important since dispatcher will check for document type first
@dispatcher.message_handler(content_types=ContentTypes.DOCUMENT)
async def file_await(message: Message):
    await message.answer(FILE_IN_PROCESS)


@dispatcher.message_handler(content_types=ContentTypes.ANY)
async def not_document(message: Message):
    await message.reply(TYPE_ERROR)
