from application.repositories import UserRepository
from application.services import UserService

from components.base import async_session


class Gateways:
    user_repository = UserRepository(async_session)
    user_service = UserService(user_repository)
