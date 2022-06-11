from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_NAME: str = "watson"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "jesus"
    DATABASE_PASS: str = ""

    TELEGRAM_API_TOKEN: str = ""
    SECONDS_PER_DAY: int = 86400

    @property
    def db_url(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DATABASE_USER,
            password=self.DATABASE_PASS,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            name=self.DATABASE_NAME,
        )


settings = Settings()
