from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
if TYPE_CHECKING:
    from traffcap.model import InboundRequest


class InboundRequestHeader(SQLModel, table=True):
    """
    The InboundRequestHeader model represents all request headers intercepted
    through the main `/r` endpoint.
    """
    __tablename__: str = "inbound_request_headers"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(max_length=255)
    value: str = Field(max_length=255)
    inbound_request_id: int = Field(default=None, foreign_key="inbound_requests.id")
    inbound_request: "InboundRequest" = Relationship(back_populates="inbound_request_headers")
