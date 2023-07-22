from typing import Optional
from .repository import Repository
from traffcap.model import User
from sqlalchemy import select, ScalarResult


class UserRepository(Repository):
    @classmethod
    async def add_a_test_user(cls) -> Optional[User]:
        user = None
        async with cls.session() as session:
            async with session.begin():
                user = User(
                    email="centurix@gmail.com",
                    fullname="Chris Read"
                )
                session.add(user)

        return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        user = None
        async with cls.session() as session:
            user = await session.get(User, user_id)

        return user

    @classmethod
    async def get_all_users(cls) -> ScalarResult[User]:
        async with cls.session() as session:
            return await session.scalars(select(User))
