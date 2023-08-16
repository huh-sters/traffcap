from pydantic import BaseModel


class RuleBase(BaseModel):
    rule: str


class RuleCreate(RuleBase):
    rule: str = ".*"


class Rule(RuleBase):
    id: int

    class Config:
        from_attributes = True
        resource_name: str = "rule"
        resource_id: str = "id"
