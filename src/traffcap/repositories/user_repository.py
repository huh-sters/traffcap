from typing import List
from .repository import Repository
from traffcap.model import User


class UserRepository(Repository):
    @classmethod
    async def add_a_test_user(cls) -> User:
        async with cls.session() as session:
            user = User(
                email="centurix@gmail.com",
                fullname="Chris Read"
            )
            session.add(user)
            session.commit()

            return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User:
        async with cls.session() as session:
            return session.get(User, user_id)

    @classmethod
    async def get_all_users(cls) -> List[User]:
        async with cls.session() as session:
            return session.query(User).all()
