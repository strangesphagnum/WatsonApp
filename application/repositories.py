import logging

from models import User
from application.serializers import UserData


class HandlersRepository:
    def __init__(self, db_session):
        logging.info("HandlersRepository instance initialized")
        self.db_session = db_session

    async def create_user(self, user_data: UserData) -> None:
        async with self.db_session() as session:
            user = User(
                telegram_user_id=user_data.telegram_user_id,
                telegram_chat_id=user_data.telegram_chat_id,
            )
            session.add(user)
            await session.commit()
