from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import Rule


class Match(SQLModel, table=True):
    __tablename__: str = "match"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    # Parent ID is used to build the tree, not to query by
    parent_id: Optional[int] = Field(default=None)
    rule_id: int = Field(default=None, foreign_key="rule.id")

    match_type: str = Field(max_length=255, default="")
    key: Optional[str] = Field(max_length=255, default=None)
    pattern: str = Field(max_length=255)
    invert: bool = Field(default=False)

    rule: "Rule" = Relationship(back_populates="matches")
