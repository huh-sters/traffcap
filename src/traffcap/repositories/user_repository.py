from typing import Optional, Sequence
from .repository import Repository
from traffcap.model import User
from sqlalchemy import select


class UserRepository(Repository):
    @classmethod
    async def add_a_test_user(cls) -> Optional[User]:
        user = User(
            email="centurix@gmail.com",
            fullname="Chris Read"
        )
        async with cls.session() as session:
            session.add(user)
            await session.commit()

        return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        user = None
        async with cls.session() as session:
            user = await session.get(User, user_id)

        return user

    @classmethod
    async def get_all_users(cls) -> Sequence[User]:
        async with cls.session() as session:
            results = await session.scalars(
                select(User)
            )
            return results.all()

        return []
