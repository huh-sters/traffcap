from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .rule import RuleModel


class RuleMatchModel(Base):
    __tablename__: str = "rule_matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_id: Mapped[str] = mapped_column(ForeignKey("rules.id"))
    match_type: Mapped[int] = mapped_column(Integer)
    match: Mapped[str] = mapped_column(String(255))
    rule: Mapped["RuleModel"] = relationship(back_populates="rule_matches")  # noqa: F821
