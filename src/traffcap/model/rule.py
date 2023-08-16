from typing import List
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from traffcap.model import Base, OutboundResponseModel


class RuleModel(Base):
    __tablename__: str = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule: Mapped[str] = mapped_column(String(255))
    outbound_responses: Mapped[List[OutboundResponseModel]] = relationship(  # noqa: F821
        back_populates="rule"
    )
