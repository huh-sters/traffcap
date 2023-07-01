from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class Rule(Base):
    __tablename__: str = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule: Mapped[str] = mapped_column(String(255))
