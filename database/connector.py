import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from models import Base


class DatabaseConnector:
    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if DatabaseConnector._instance is None:
            DatabaseConnector._instance = object.__new__(cls)
        return DatabaseConnector._instance

    def __init__(self):
        DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
        DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
        DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
        DATABASE_NAME = os.getenv('DATABASE_NAME', 'option_tracker')

        DATABASE_URL = f'postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def __aenter__(self):
        self.session = await self.sessionmaker()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()
