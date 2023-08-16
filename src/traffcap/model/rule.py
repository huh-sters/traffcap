from typing import List
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .outbound_response import OutboundResponseModel


class RuleModel(Base):
    __tablename__: str = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule: Mapped[str] = mapped_column(String(255))
    outbound_responses: Mapped[List["OutboundResponseModel"]] = relationship(  # noqa: F821
        back_populates="rule"
    )
