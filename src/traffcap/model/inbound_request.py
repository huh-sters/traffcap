from typing import Optional
from sqlmodel import Field, SQLModel
from fastapi import Request
from enum import Enum
from fastapi.encoders import jsonable_encoder
import json


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


class InboundRequest(SQLModel, table=True):
    __tablename__: str = "inbound_requests"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint_code: str = Field(max_length=255)
    method: str = Field(max_length=10)
    headers: str = Field(max_length=1024)
    query_params: str = Field(max_length=255)
    body: str = Field(max_length=255)

    @classmethod
    async def from_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> "InboundRequest":
        return cls(
            endpoint_code=endpoint_code,
            method=HTTPVerbs[request.method],
            headers=json.dumps(jsonable_encoder(request.headers)),
            query_params=json.dumps(jsonable_encoder(request.query_params)),
            body=await request.body()
        )
