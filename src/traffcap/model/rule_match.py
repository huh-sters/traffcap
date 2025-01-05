from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .rule import Rule


class RuleMatch(SQLModel, table=True):
    __tablename__: str = "rule_matches"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(default=None, foreign_key="rules.id")
    match_type: int
    match: str = Field(max_length=255)
    rule: Rule = Relationship(back_populates="rule_matches")
