from aiogram import Bot

from settings import settings
from base import async_session

bot = Bot(token=settings.TELEGRAM_API_TOKEN)
bot["db"] = async_session
