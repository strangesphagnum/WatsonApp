from settings import test_settings

from telethon.tl.custom.conversation import Conversation

from application.messages import WELCOME


async def test_welcome_message(telegram_client) -> Conversation:
    async with telegram_client.conversation(
        test_settings.TELEGRAM_BOT_NAME, timeout=10, max_messages=10000
    ) as conv:
        conv: Conversation
        await conv.send_message("/start")
        response = await conv.get_response()

        assert response.message.text == WELCOME
