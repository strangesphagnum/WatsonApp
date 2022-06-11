import logging
from typing import Optional
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Update

from models import User


class UserRepository:
    def __init__(self, db_session):
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

    async def update_user_last_uploaded(self, telegram_user_id: int) -> None:
        # TODO: make query simplier
        current_date = datetime.now()
        stm = select(User).where(User.telegram_user_id == telegram_user_id)

        async with self.db_session() as session:
            user_raw = await session.execute(stm)
            user = user_raw.scalar()
            user.last_uploaded = current_date
            await session.commit()
