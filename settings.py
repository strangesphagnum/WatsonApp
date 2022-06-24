from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_NAME: str = "watson"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "jesus"
    DATABASE_PASS: str = ""

    @property
    def db_dsn(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DATABASE_USER,
            password=self.DATABASE_PASS,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            name=self.DATABASE_NAME,
        )


class RabbitMQSettings(BaseSettings):
    AMQP_PORT: int = 5672
    AMQP_LOGIN: str = "guest"
    AMQP_PASSWORD: str = "guest"
    AMQP_TELEGRAM_QUEUE_NAME: str = "telegram-chat-document"
    AMQP_HOST: str = "localhost"

    @property
    def rabbit_dsn(self) -> str:
        return "amqp://{user}:{password}@{host}/".format(
            user=self.AMQP_LOGIN,
            password=self.AMQP_PASSWORD,
            host=self.AMQP_HOST,
        )


class TelegramSettings(BaseSettings):
    TELEGRAM_API_TOKEN: str = ""


class CommonSettings(DatabaseSettings, RabbitMQSettings, TelegramSettings):
    DEBUG: bool = True


settings = CommonSettings()
