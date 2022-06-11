from application.repositories import UserRepository
from application.services import HandlersService

from base import async_session


class Gateways:
    handlers_repository = UserRepository(async_session)
    handlers_service = HandlersService(handlers_repository)
