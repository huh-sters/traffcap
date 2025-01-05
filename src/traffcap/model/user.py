from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__: str = "users"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255)
    fullname: str = Field(max_length=32)
