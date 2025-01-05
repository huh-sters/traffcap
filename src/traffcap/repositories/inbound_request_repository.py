from typing import Sequence
from .repository import Repository
from fastapi import Request
from traffcap.model import InboundRequest
from sqlmodel import select


class InboundRequestRepository(Repository):
    @classmethod
    async def store_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> None:
        async with cls.session() as session:
            session.add(await InboundRequest.from_request(endpoint_code, request))
            await session.commit()

    @classmethod
    async def get_all_inbound_requests(cls) -> Sequence[InboundRequest]:
        async with cls.session() as session:
            results = await session.scalars(
                select(InboundRequest)
            )
            return results.all()

        return []
