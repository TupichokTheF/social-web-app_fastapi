from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

from typing import Annotated

from models import Base
from core.settings import settings

from redis import Redis

class Database:

    def __init__(self):
        self._engine = create_async_engine(str(settings.DATABASE_URL))
        self._session = async_sessionmaker(self._engine)

    async def get_session(self):
        async with self._session() as session:
            yield session

    async def init_database(self):
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def dispose_database(self):
        await self._engine.dispose()

database = Database()

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

def get_redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

RedisDep = Annotated[Redis, Depends(get_redis)]