from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from .base import Base


class InboundRequestModel(Base):
    __tablename__: str = "inbound_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_code: Mapped[str] = mapped_column(String(255))
    method: Mapped[str] = mapped_column(String(10))
    headers: Mapped[str] = mapped_column(String(1024))
    query_params: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
