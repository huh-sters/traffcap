from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .rule import RuleModel


class OutboundResponseModel(Base):
    __tablename__: str = "outbound_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_id: Mapped[str] = mapped_column(ForeignKey("rules.id"))
    content_type: Mapped[str] = mapped_column(String(32))
    template: Mapped[str] = mapped_column(String(1024))
    rule: Mapped["RuleModel"] = relationship(back_populates="outbound_responses")  # noqa: F821
