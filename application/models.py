from enum import IntEnum

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(
        "id", sa.BigInteger(), primary_key=True, unique=True, autoincrement=True
    )
    telegram_user_id = sa.Column(
        "telegram_user_id", sa.Integer(), nullable=False, unique=True, index=True
    )
    telegram_chat_id = sa.Column("telegram_chat_id", sa.Integer(), nullable=False)
    registered_at = sa.Column(
        "registered_at",
        sa.TIMESTAMP(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    last_uploaded = sa.Column("last_uploaded", sa.TIMESTAMP(timezone=False))


class Mutation(Base):
    __tablename__ = "mutations"

    id = sa.Column(
        "id", sa.BigInteger(), primary_key=True, unique=True, autoincrement=True
    )
    rsid = sa.Column("rsid", sa.String(16), nullable=False, unique=True, index=True)
    link = sa.Column("link", sa.String())
