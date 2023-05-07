from pydantic import BaseModel


class EndpointBase(BaseModel):
    code: str


class EndpointCreate(EndpointBase):
    pass


class Endpoint(EndpointBase):
    id: int

    class Config:
        orm_mode = True
