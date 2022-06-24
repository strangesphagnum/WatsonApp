""" Tests are currently in progress
"""
import asyncio
import threading

import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from aiogram import executor

from settings import test_settings
from application.dispatcher import dispatcher


@pytest.fixture(autouse=True, scope="session")
def bot():
    import application.handlers  # noqa

    stop_event = threading.Event()
    thread = threading.Thread(
        target=executor.start_polling(dispatcher, skip_updates=True),
        kwargs={"stop_event": stop_event},
    )
    thread.start()
    yield
    stop_event.set()
    thread.join()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def telegram_client():
    api_id = test_settings.TELEGRAM_APP_ID
    api_hash = test_settings.TELEGRAM_APP_HASH
    session_str = test_settings.TELEGRAM_APP_SESSION

    client = TelegramClient(
        StringSession(session_str), api_id, api_hash, sequential_updates=True
    )
    await client.connect()
    await client.get_me()
    await client.get_dialogs()

    yield client

    await client.disconnect()
    await client.disconnected
