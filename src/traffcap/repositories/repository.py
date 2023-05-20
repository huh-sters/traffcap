from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from typing import Optional
import asyncio


class Repository:
    class session:
        engine: Optional[AsyncEngine] = None

        def __init__(self):
            pass

        async def __aenter__(self):
            async_session = async_sessionmaker(
                self.engine,
                expire_on_commit=False
            )
            return async_session()

        async def __aexit__(self, exc_type, exc, tb):
            pass


    @classmethod
    def create_connection(cls) -> None:
        # Create an async session for the main application
        cls.session.engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)

    @classmethod
    async def _upgrade(cls) -> None:
        # Perform any migrations
        # async with cls.session.engine.begin() as connection:
        #     await connection.run_sync(Base.metadata.drop_all)
        #     await connection.run_sync(Base.metadata.create_all)
        pass

    @classmethod
    def migrate_up(cls) -> None:
        # Migrate up the database
        asyncio.run(cls._upgrade())

    @classmethod
    def migrate_down(cls) -> None:
        # Migrate down, nothing here yet
        pass
