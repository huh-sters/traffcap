from pydantic import BaseModel, Field


class OutboundResponseBase(BaseModel):
    rule_id: str
    content_type: str
    template: str


class OutboundResponseCreate(OutboundResponseBase):
    pass


class OutboundResponse(OutboundResponseBase):
    id: int = Field(json_schema_extra={
        "resource_id": True
    })

    class Config:
        from_attributes = True
        resource_name: str = "outbound_response"
        resource_id: str = "id"
