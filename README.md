# About this repo
This is a core part of Watson project that responsible for interaction with client and publishing user's chat id and uploaded document id into the queue.

Provides:
- tg interface
- db models
- rabbitmq message publishing

Built on:
- [AIOGram](https://docs.aiogram.dev)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/)
- [aio-pika](https://aio-pika.readthedocs.io)

# Usage
For client usage please visit [mutations seeker bot](https://t.me/mutations_seeker_bot), start the bot and follow the instructions.

*Currently unavailable. Please, contact [developer](https://t.me/poteryannaya_zakladka) for testing purposes*

For developing purposes:
1. Get your own bot token via [Telegram BotFather](https://t.me/BotFather)
2. Build image with docker (`docker build .`)
3. Start docker container with envs provided. I.e.: `docker run -e DATABASE_HOST='127.0.0.1' -e TELEGRAM_API_TOKEN='foo' [image]`

Alternatively you can use docker-compose or start directly by `main.py` or start in any convenient way.

# About Watson Project
**Work in progress!**

Named after [James Watson](https://en.wikipedia.org/wiki/James_Watson) Watson project provides simple tool availiable in telegram for user's genome mutations check.

It allows user to upload .23andme type genome data and seek for important mutations based on [OpenSNP](https://opensnp.org) source.

The founded mutations returns as message in telegram directly to user with clinical data provided.

# See other repos
- [Data Engineering pipelines](https://github.com/strangesphagnum/WatsonPipelines)
- [Docker-compose](https://github.com/strangesphagnum/WatsonCore)