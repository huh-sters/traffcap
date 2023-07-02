from pydantic import BaseModel
from fastapi import Request
import json
from fastapi.encoders import jsonable_encoder
from enum import Enum


class HTTPVerbs(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    TRACE = "TRACE"

    @classmethod
    def to_list(cls):
        return [el.value for el in cls]


class InboundRequestBase(BaseModel):
    endpoint_code: str
    method: HTTPVerbs
    headers: str
    query_params: str
    body: bytes

    @classmethod
    async def from_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> "InboundRequestBase":
        return cls(
            endpoint_code=endpoint_code,
            method=request.method,
            headers=json.dumps(jsonable_encoder(request.headers)),
            query_params=json.dumps(jsonable_encoder(request.query_params)),
            body=await request.body()
        )


class InboundRequestCreate(InboundRequestBase):
    pass


class InboundRequest(InboundRequestBase):
    id: int

    class Config:
        orm_mode = True
