from pydantic import BaseModel


class RuleBase(BaseModel):
    rule: str


class RuleCreate(RuleBase):
    rule: str = ".*"


class Rule(RuleBase):
    id: int

    class Config:
        orm_mode = True
