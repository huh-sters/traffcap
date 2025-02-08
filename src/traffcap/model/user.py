from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class UserBase(SQLModel):
    email: str = Field(max_length=255)
    fullname: str = Field(max_length=32)


class User(UserBase, table=True):
    __tablename__: str = "user"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserPublic(UserBase):
    id: int
