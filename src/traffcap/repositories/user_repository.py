from typing import Optional
from .repository import Repository, inject_session
from traffcap.model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult


class UserRepository(Repository):
    @classmethod
    @inject_session
    async def add_a_test_user(cls, session: AsyncSession) -> User:
        async with session.begin():
            user = User(
                email="centurix@gmail.com",
                fullname="Chris Read"
            )
            session.add(user)

            return user

    @classmethod
    @inject_session
    async def get_user_by_id(
        cls,
        user_id: int,
        session: AsyncSession
    ) -> Optional[User]:
        return await session.get(User, user_id)

    @classmethod
    @inject_session
    async def get_all_users(cls, session: AsyncSession) -> ScalarResult[User]:
        return await session.scalars(select(User))
