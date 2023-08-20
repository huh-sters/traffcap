from pydantic import BaseModel, Field, ConfigDict


class OutboundResponseBase(BaseModel):
    rule_id: int
    content_type: str
    template: str


class OutboundResponseCreate(OutboundResponseBase):
    pass


class OutboundResponse(OutboundResponseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(json_schema_extra={
        "resource_id": True
    })
