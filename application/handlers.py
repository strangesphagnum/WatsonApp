from aiogram.types import Message, ContentTypes

from application.dispatcher import dispatcher
from application.messages import (
    WELCOME,
    TYPE_ERROR,
    FILE_ADDED_TO_QUEUE,
    TOO_MANY_ATTEMPTS,
)
from application.containers import Gateways
from application.exceptions import TooManyAttemptsError


@dispatcher.message_handler(commands=["start", "help"])
async def register_user(message: Message, user_service=Gateways.user_service) -> None:
    await user_service.create_user_if_none(message=message)
    await message.reply(WELCOME)


# Handlers order is important since dispatcher should check for document type first
@dispatcher.message_handler(content_types=ContentTypes.DOCUMENT)
async def add_file_to_queue(message: Message, user_service=Gateways.user_service):
    try:
        await user_service.check_uploaded_date(message)
        await user_service.update_uploaded_date(message)
        await message.answer(FILE_ADDED_TO_QUEUE)
    except TooManyAttemptsError:
        await message.answer(TOO_MANY_ATTEMPTS)


@dispatcher.message_handler(content_types=ContentTypes.ANY)
async def not_document(message: Message):
    await message.reply(TYPE_ERROR)
