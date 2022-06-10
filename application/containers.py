from application.repositories import HandlersRepository
from application.services import HandlersService

from base import async_session


class Gateways:
    handlers_repository = HandlersRepository(async_session)
    handlers_service = HandlersService(handlers_repository)
