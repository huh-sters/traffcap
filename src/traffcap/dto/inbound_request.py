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


class InboundRequestBase(BaseModel):
    endpoint_code: str
    verb: HTTPVerbs
    headers: str
    query_params: str
    body: bytes

    @classmethod
    async def from_request(
        cls,
        endpoint_code: str,
        verb: HTTPVerbs,
        request: Request
    ) -> "InboundRequestBase":
        return cls(
            endpoint_code=endpoint_code,
            verb=verb,
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
