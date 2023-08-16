from pydantic import BaseModel, Field


class RuleBase(BaseModel):
    rule: str


class RuleCreate(RuleBase):
    rule: str = ".*"


class Rule(RuleBase):
    id: int = Field(json_schema_extra={
        "resource_id": True
    })

    class Config:
        from_attributes = True
        resource_name: str = "rule"
        resource_id: str = "id"
