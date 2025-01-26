from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import Rule


class OutboundResponse(SQLModel, table=True):
    __tablename__: str = "outbound_response"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    content_type: str = Field(max_length=32)
    template: str = Field(max_length=1024)

    rule_id: int = Field(default=None, foreign_key="rule.id")
    rule: "Rule" = Relationship(back_populates="outbound_responses")
