from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class User(Base):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    fullname: Mapped[str] = mapped_column(String(32))
