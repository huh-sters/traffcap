from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import Rule


class MatchBase(SQLModel):
    parent_id: Optional[int] = Field(default=None)
    rule_id: int = Field(default=None, foreign_key="rule.id")
    match_type: str = Field(max_length=255, default="")
    key: Optional[str] = Field(max_length=255, default=None)
    pattern: str = Field(max_length=255)
    invert: bool = Field(default=False)


class Match(MatchBase, table=True):
    __tablename__: str = "match"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    rule: "Rule" = Relationship(back_populates="matches")


class MatchPublic(MatchBase):
    id: int
