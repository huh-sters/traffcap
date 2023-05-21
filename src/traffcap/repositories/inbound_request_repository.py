from .repository import Repository, inject_session
from fastapi import Request
from traffcap.dto import InboundRequestCreate
from sqlalchemy.ext.asyncio import AsyncSession


class InboundRequestRepository(Repository):
    @classmethod
    @inject_session
    async def store_request(
        cls,
        endpoint_code: str,
        request: Request,
        session: AsyncSession
    ) -> None:
        """
        Store the components of the request
        """
        async with session.begin():
            session.add(await InboundRequestCreate.from_request(
                endpoint_code,
                request
            ))
