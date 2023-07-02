from typing import Optional
from .repository import Repository
from traffcap.model import User
from sqlalchemy import select, ScalarResult


class UserRepository(Repository):
    @classmethod
    async def add_a_test_user(cls) -> User:
        session = await cls.new_session()
        async with session.begin():
            user = User(
                email="centurix@gmail.com",
                fullname="Chris Read"
            )
            session.add(user)

            return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        session = await cls.new_session()
        return await session.get(User, user_id)

    @classmethod
    async def get_all_users(cls) -> ScalarResult[User]:
        session = await cls.new_session()
        return await session.scalars(select(User))
