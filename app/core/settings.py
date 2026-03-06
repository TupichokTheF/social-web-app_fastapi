from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

from datetime import timedelta

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DATABASE: str = ""

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DATABASE
        )

    ALGORITHM_OF_CIFER: str = ""
    JWT_SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=1)

    REDIS_HOST: str = ""
    REDIS_PORT: str = ""

settings = Settings()