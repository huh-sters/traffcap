from typing import Optional
from .repository import Repository
from traffcap.dto import User
from traffcap.model import UserModel
from sqlalchemy import select
from typing import List


class UserRepository(Repository):
    @classmethod
    async def add_a_test_user(cls) -> Optional[User]:
        user = None
        async with cls.session() as session:
            session.add(
                UserModel(
                    email="centurix@gmail.com",
                    fullname="Chris Read"
                )
            )
            await session.commit()

        return User.model_validate(user)

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> Optional[User]:
        user = None
        async with cls.session() as session:
            user = await session.get(UserModel, user_id)

        return User.model_validate(user)

    @classmethod
    async def get_all_users(cls) -> List[User]:
        users = []
        async with cls.session() as session:
            results = await session.scalars(
                select(UserModel)
            )
            for user in results.all():
                users.append(User.model_validate(user))

        return users
