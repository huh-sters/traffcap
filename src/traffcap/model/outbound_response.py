from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from traffcap.model import Base


class OutboundResponse(Base):
    __tablename__: str = "outbound_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_id: Mapped[str] = mapped_column(ForeignKey("rules.id"))
    content_type: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(String(1024))
    rule: Mapped["Rule"] = relationship(back_populates="children")  # noqa: F821
