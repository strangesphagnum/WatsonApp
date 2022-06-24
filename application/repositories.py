from typing import Optional
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.models import User
from components.queue import AMQPQueueConstructor


# TODO: redesign abstract repo for this case
class AbstractRepository:
    pass


class SQLRepository(AbstractRepository):
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


class RabbitRepository(AbstractRepository):
    def __init__(self, amqp_instance: AMQPQueueConstructor):
        self.amqp_instance = amqp_instance

    async def publish_record(self, message: str) -> None:
        await self.amqp_instance.publish_message(message)
