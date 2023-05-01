from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class Endpoint(Base):
    __tablename__: str = "endpoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(255))
