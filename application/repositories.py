import logging
from typing import Optional

from sqlalchemy.future import select

from models import User
from application.serializers import UserData


class HandlersRepository:
    def __init__(self, db_session):
        logging.info("HandlersRepository instance initialized")
        self.db_session = db_session

    async def create_user(self, telegram_user_id: int, telegram_chat_id: int) -> None:
        async with self.db_session() as session:
            user = User(
                telegram_user_id=telegram_user_id,
                telegram_chat_id=telegram_chat_id,
            )
            session.add(user)
            await session.commit()

    async def get_user(self, telegram_user_id: int) -> Optional[User]:
        stm = select(User).where(User.telegram_user_id == telegram_user_id)

        async with self.db_session() as session:
            user_raw = await session.execute(stm)
            user = user_raw.scalar()

        if user is None:
            return None

        return user
