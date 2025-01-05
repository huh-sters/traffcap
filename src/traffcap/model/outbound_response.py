from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from traffcap.model import Rule


class OutboundResponse(SQLModel, table=True):
    __tablename__: str = "outbound_responses"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(default=None, foreign_key="rules.id")
    content_type: str = Field(max_length=32)
    template: str = Field(max_length=1024)
    rule: Rule = Relationship(back_populates="outbound_responses")
