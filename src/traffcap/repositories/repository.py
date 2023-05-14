from collections.abc import Generator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import Session
from contextlib import contextmanager
from traffcap.model import Base
import asyncio


class Repository:
    engine = None

    class session:
        def __init__(self):
            pass

        async def __aenter__(self):
            self.engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
            async_session = async_sessionmaker(self.engine, expire_on_commit=False)
            return async_session()

        async def __aexit__(self, exc_type, exc, tb):
            pass


    # @classmethod
    # @contextmanager
    # async def session(cls):
    #     cls.engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
    #     async_session = async_sessionmaker(cls.engine, expire_on_commit=False)
    #     yield async_session()

    @classmethod
    async def upgrade(cls) -> None:
        engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
        # Base.metadata.create_all(engine)

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
