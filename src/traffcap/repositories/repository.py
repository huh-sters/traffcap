from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine
)
from alembic import command
from alembic.config import Config
from typing import Optional
from types import TracebackType
from migrations.url import generate_db_url

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


class Repository:
    engine: Optional[AsyncEngine] = None

    # AsyncSession context manager
    class session:
        def __init__(self) -> None:
            self.session: Optional[AsyncSession] = None

        async def __aenter__(self) -> AsyncSession:
            if not Repository.engine:
                raise Exception("Database not connected")

            self.session = async_sessionmaker(
                bind=Repository.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )()

            return self.session

        async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc: Optional[BaseException],
            tb: Optional[TracebackType]
        ) -> bool:
            if self.session:
                await self.session.close()

            return True

    @classmethod
    def create_connection(cls) -> None:
        # Create an async session for the main application
        cls.engine = create_async_engine(generate_db_url(), echo=False)

    @classmethod
    def migrate_up(cls) -> None:
        # Migrate up the database
        config = Config("src/alembic.ini")
        command.upgrade(config, "head")

    @classmethod
    def migrate_down(cls) -> None:
        # Migrate down, not necessary
        pass
