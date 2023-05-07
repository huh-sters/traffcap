from typing import List
from .repository import Repository
from traffcap.model import User
from sqlalchemy import select


class UserRepository(Repository):
    @classmethod
    def add_a_test_user(cls) -> User:
        with cls.session() as session:
            user = User(
                email="centurix@gmail.com",
                fullname="Chris Read"
            )
            session.add(user)
            session.commit()

            return user

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:
        with cls.session() as session:
            return session.get(User, user_id)

    @classmethod
    def get_all_users(cls) -> List[User]:
        with cls.session() as session:
            return session.query(User).all()
