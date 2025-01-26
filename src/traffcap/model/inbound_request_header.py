from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import InboundRequest


class InboundRequestHeaderBase(SQLModel):
    key: str = Field(max_length=255)
    value: str = Field(max_length=255)


class InboundRequestHeader(InboundRequestHeaderBase, table=True):
    """
    The InboundRequestHeader model represents all request headers intercepted
    through the main `/r` endpoint.
    """
    __tablename__: str = "inbound_request_header"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    inbound_request_id: int = Field(default=None, foreign_key="inbound_request.id")
    inbound_request: "InboundRequest" = Relationship(back_populates="headers")


class InboundRequestHeaderCreate(InboundRequestHeaderBase):
    pass


class InboundRequestHeaderPublic(InboundRequestHeaderBase):
    id: int


class InboundRequestHeaderUpdate(SQLModel):
    key: str
    value: str
