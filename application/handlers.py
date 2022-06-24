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


@dispatcher.message_handler(commands=["start"])
async def register_user(message: Message, user_service=Gateways.user_service):
    """Write user with telegram_user_id and telegram_chat_id cols if user don't exists"""
    await user_service.create_if_none(message=message)
    await message.reply(WELCOME)


# Handlers order is important since dispatcher should check for document type first
@dispatcher.message_handler(content_types=ContentTypes.DOCUMENT)
async def add_file_to_queue(message: Message, user_service=Gateways.user_service, rabbit_service=Gateways.user_rabbit_service):
    """
    1. Works if message type is Document
    2. Check if uploaded date user's record delta with current dt is no more than 1 day
    3. Send message for both success and unsucess cases
    """
    try:
        await user_service.check_uploaded_date(message=message)
        await user_service.update_uploaded_date(message=message)
        await rabbit_service.publish_message(message=message)
        await message.answer(FILE_ADDED_TO_QUEUE)
    except TooManyAttemptsError:
        await message.answer(TOO_MANY_ATTEMPTS)


@dispatcher.message_handler(content_types=ContentTypes.ANY)
async def not_document(message: Message):
    """
    1. Works if message type doesn't satisfy 'Document' type condition
    2. Send message that informs user about wrong message type
    """
    await message.reply(TYPE_ERROR)
