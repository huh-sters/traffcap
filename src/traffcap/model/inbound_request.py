from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from fastapi import Request
from enum import Enum
from fastapi.encoders import jsonable_encoder
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


class InboundRequestBase(SQLModel):
    endpoint_code: str = Field(max_length=255)
    method: str = Field(max_length=10)
    body: str = Field(max_length=255)


class InboundRequest(InboundRequestBase, table=True):
    """
    The InboundRequest model represents all requests intercepted
    through the main `/r` endpoint. This records the endpoint, HTTP verb
    headers, query parameters and the request body.
    """
    __tablename__: str = "inbound_requests"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    query_params: list["InboundRequestQueryParam"] = Relationship(back_populates="inbound_request", sa_relationship_kwargs={"lazy": "joined"})
    headers: list["InboundRequestHeader"] = Relationship(back_populates="inbound_request", sa_relationship_kwargs={"lazy": "joined"})

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


class InboundRequestCreate(InboundRequestBase):
    pass


class InboundRequestPublic(InboundRequestBase):
    id: int


class InboundRequestUpdate(SQLModel):
    endpoint_code: str
    method: str
    body: str
