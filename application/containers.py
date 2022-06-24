from application.repositories import RabbitRepository, UserRepository
from application.services import UserService, UserRabbitService

from components.base import async_session
from components.queue import chat_document_amqp


class Gateways:
    user_repository = UserRepository(async_session)
    user_service = UserService(user_repository)
    user_rabbit_repository = RabbitRepository(chat_document_amqp)
    user_rabbit_service = UserRabbitService(user_rabbit_repository)
