from pydantic import BaseModel, Field, ConfigDict


class RuleBase(BaseModel):
    rule: str


class RuleCreate(RuleBase):
    rule: str = ".*"


class Rule(RuleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(json_schema_extra={
        "resource_id": True
    })
