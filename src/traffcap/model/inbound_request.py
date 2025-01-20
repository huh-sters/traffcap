from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from fastapi import Request
from starlette.datastructures import URL
from traffcap.model import HTTPVerbs
from datetime import datetime, timezone
if TYPE_CHECKING:
    from traffcap.model import (
        InboundRequestHeader,
        InboundRequestQueryParam
    )


class InboundRequestBase(SQLModel):
    endpoint_code: str = Field(max_length=255)
    method: str = Field(max_length=10)
    body: str = Field(max_length=255)
    source_host: str = Field(max_length=255)
    source_port: int
    request_line: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


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
            body=(await request.body()).decode(),
            source_host=request.client.host,
            source_port=request.client.port,
            request_line=str(request.url)
        )

    @property
    def url(self) -> URL:
        return URL(self.request_line)

class InboundRequestPublic(InboundRequestBase):
    id: int
