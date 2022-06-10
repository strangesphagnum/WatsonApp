from aiogram.types import Message, ContentTypes

from application.dispatcher import dispatcher
from application.messages import WELCOME, TYPE_ERROR, FILE_IN_PROCESS
from application.containers import Gateways


@dispatcher.message_handler(commands=["start", "help"])
async def register_user(
    message: Message, handlers_service=Gateways.handlers_service
) -> None:
    await handlers_service.create_user(message=message)
    await message.reply(WELCOME)


# The order is important since dispatcher will check for document type first
@dispatcher.message_handler(content_types=ContentTypes.DOCUMENT)
async def file_await(message: Message):
    await message.answer(FILE_IN_PROCESS)


@dispatcher.message_handler(content_types=ContentTypes.ANY)
async def not_document(message: Message):
    await message.reply(TYPE_ERROR)
