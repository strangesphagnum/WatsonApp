# About this repo
This is a core part of Watson project that responsible for interaction with client and publishing user's chat id and uploaded document id into the queue.

Provides:
- tg interface
- db models
- rabbitmq message publishing

Built on
- [AIOGram](https://docs.aiogram.dev)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/)
- [aio-pika](https://aio-pika.readthedocs.io)

# Usage
Please visit [mutations seeker bot](https://t.me/mutations_seeker_bot)

Start the bot and follow the instructions.

# About Watson Project
*Work in progress!*

Named after [James Watson](https://en.wikipedia.org/wiki/James_Watson) Watson project provides simple tool availiable in telegram for user's genome mutations check.

It allows user to upload .23andme type genome data and seek for important mutations based on [OpenSNP](https://opensnp.org) source.

The founded mutations returns as message in telegram directly to user with clinical data provided.

# See other repos
- [Data Engineering pipelines](https://github.com/strangesphagnum/WatsonPipelines)
- [Docker-compose](https://github.com/strangesphagnum/WatsonCore)