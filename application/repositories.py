from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


# TODO: rethink abstract repo for this case
class AbstractRepository(ABC):
    @abstractmethod
    def create_record(self):
        raise NotImplementedError

    @abstractmethod
    def get_record(self):
        raise NotImplementedError


class UserRepository(AbstractRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    async def create_record(self, telegram_user_id: int, telegram_chat_id: int) -> None:
        async with self.db_session() as session:
            user = User(
                telegram_user_id=telegram_user_id,
                telegram_chat_id=telegram_chat_id,
            )
            session.add(user)
            await session.commit()

    async def get_record(self, telegram_user_id: int) -> Optional[User]:
        stm = select(User).where(User.telegram_user_id == telegram_user_id)

        async with self.db_session() as session:
            user_raw = await session.execute(stm)
            user = user_raw.scalar()

        if user is None:
            return None

        return user

    async def update_record_last_uploaded(self, telegram_user_id: int) -> None:
        stmt = (
            update(User)
            .where(User.telegram_user_id == telegram_user_id)
            .values(last_uploaded=datetime.now())
        )

        async with self.db_session() as session:
            await session.execute(stmt)
            await session.commit()
