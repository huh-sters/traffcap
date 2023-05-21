from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from typing import Optional
import asyncio


def inject_session(f):
    """
    Poor mans dependency injection. Inject a session into the repository call.
    """
    async def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return await f(*args, **kwargs)

        if not Repository.engine:
            raise Exception("Database not connected")

        async_session = async_sessionmaker(
            Repository.engine,
            expire_on_commit=False
        )
        return await f(*args, **kwargs, session=async_session())

    return wrapper


class Repository:
    engine: Optional[AsyncEngine] = None

    @classmethod
    def create_connection(cls) -> None:
        # Create an async session for the main application
        cls.engine = create_async_engine(
            "sqlite+aiosqlite:///test.db",
            echo=True
        )

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
