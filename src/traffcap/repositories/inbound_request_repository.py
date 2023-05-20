from .repository import Repository
from fastapi import Request
from traffcap.dto import InboundRequestCreate


class InboundRequestRepository(Repository):
    @classmethod
    async def store_request(cls, endpoint_code: str, request: Request) -> None:
        """
        Store the components of the request
        """
        async with cls.session() as session:
            await session.add(await InboundRequestCreate.from_request(endpoint_code, request))
            await session.commit()
