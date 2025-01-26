from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import Match


"""
Rules are used by Traffcap to decide how to respond to an inbound request.
"""

class Rule(SQLModel, table=True):
    __tablename__: str = "rule"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=255)
    priority: int = Field(default=0)

    content_type: str = Field(max_length=32)
    template: str = Field()

    matches: list["Match"] = Relationship(back_populates="rule", sa_relationship_kwargs={"lazy": "joined"})
