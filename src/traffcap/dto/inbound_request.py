from pydantic import BaseModel
from fastapi import Request
import json
from fastapi.encoders import jsonable_encoder


class InboundRequestBase(BaseModel):
    endpoint_code: str
    headers: str
    query_params: str
    body: str


class InboundRequestCreate(InboundRequestBase):
    pass

class InboundRequest(InboundRequestBase):
    id: int

    class Config:
        orm_mode = True

    @classmethod
    async def from_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> "InboundRequest":
        return cls(
            endpoint_code=endpoint_code,
            headers=json.dumps(jsonable_encoder(request.headers)),
            query_params=json.dumps(jsonable_encoder(request.query_params)),
            body=await request.body()
        )
