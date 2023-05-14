from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class InboundRequest(Base):
    __tablename__: str = "inbound_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_code: Mapped[str] = mapped_column(String(255))
    headers: Mapped[str] = mapped_column(String(255))
    query_params: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
