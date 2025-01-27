from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(max_length=255)
    fullname: str = Field(max_length=32)


class User(UserBase, table=True):
    __tablename__: str = "user"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int
