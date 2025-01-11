from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from fastapi import Request
from enum import Enum
from fastapi.encoders import jsonable_encoder
import json
if TYPE_CHECKING:
    from traffcap.model import (
        InboundRequestHeader,
        InboundRequestQueryParam
    )


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
    """
    The InboundRequest model represents all requests intercepted
    through the main `/r` endpoint. This records the endpoint, HTTP verb
    headers, query parameters and the request body.
    """
    __tablename__: str = "inbound_requests"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint_code: str = Field(max_length=255)
    method: str = Field(max_length=10)
    body: str = Field(max_length=255)
    inbound_request_query_params: list["InboundRequestQueryParam"] = Relationship(back_populates="inbound_request", sa_relationship_kwargs={"lazy": "joined"})
    inbound_request_headers: list["InboundRequestHeader"] = Relationship(back_populates="inbound_request", sa_relationship_kwargs={"lazy": "joined"})

    @classmethod
    async def from_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> "InboundRequest":
        return cls(
            endpoint_code=endpoint_code,
            method=HTTPVerbs[request.method],
            body=(await request.body()).decode()
        )
