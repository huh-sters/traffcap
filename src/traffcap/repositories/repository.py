from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from alembic import command
from alembic.config import Config
from typing import Optional
from migrations.url import generate_db_url


class Repository:
    engine: Optional[AsyncEngine] = None

    @classmethod
    async def new_session(cls) -> AsyncSession:
        if not Repository.engine:
            raise Exception("Database not connected")

        session = async_sessionmaker(
            Repository.engine,
            expire_on_commit=False
        )
        return session()

    @classmethod
    def create_connection(cls) -> None:
        # Create an async session for the main application
        cls.engine = create_async_engine(generate_db_url(), echo=False)

    @classmethod
    def migrate_up(cls) -> None:
        # Migrate up the database
        config = Config("alembic.ini")
        command.upgrade(config, "head")

    @classmethod
    def migrate_down(cls) -> None:
        # Migrate down, not necessary
        pass
