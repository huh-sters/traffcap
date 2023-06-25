from pydantic import BaseModel, Field
from uuid import uuid4


def new_uuid() -> str:
    return uuid4().hex


class EndpointBase(BaseModel):
    code: str


class EndpointCreate(EndpointBase):
    code: str = Field(default_factory=new_uuid)


class Endpoint(EndpointBase):
    id: int

    class Config:
        orm_mode = True
