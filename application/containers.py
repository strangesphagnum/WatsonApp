from application.repositories import RabbitRepository, SQLRepository
from application.services import SQLService, RabbitService

from components.base import async_session
from components.queue import chat_document_amqp


class Gateways:
    sql_repository = SQLRepository(async_session)
    sql_service = SQLService(sql_repository)
    user_rabbit_repository = RabbitRepository(chat_document_amqp)
    user_rabbit_service = RabbitService(user_rabbit_repository)
