from aiogram import executor

from application.dispatcher import dispatcher
import application.handlers  # noqa


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
