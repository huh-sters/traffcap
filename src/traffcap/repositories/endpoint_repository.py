from typing import Optional
from .repository import (
    Repository,
    inject_session
)
from traffcap.dto import EndpointCreate
from traffcap.model import (
    Endpoint,
    InboundRequest
)
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession


class EndpointRepository(Repository):
    @classmethod
    @inject_session
    async def get_endpoint_by_id(
        cls,
        endpoint_id: int,
        session: AsyncSession
    ) -> Optional[Endpoint]:
        return await session.get(Endpoint, endpoint_id)

    @classmethod
    @inject_session
    async def get_all_endpoints(
        cls,
        session: AsyncSession
    ) -> ScalarResult[Endpoint]:
        return await session.scalars(select(Endpoint))

    @classmethod
    @inject_session
    async def get_endpoint_by_code(
        cls,
        endpoint_code: str,
        session: AsyncSession
    ) -> Optional[Endpoint]:
        return await session.scalar(select(Endpoint).filter_by(code=endpoint_code))

    @classmethod
    @inject_session
    async def get_endpoint_traffic(
        cls,
        endpoint_code: str,
        session: AsyncSession
    ) -> ScalarResult[InboundRequest]:
        return await session.scalars(
            select(InboundRequest).filter_by(endpoint_code=endpoint_code)
        )

    @classmethod
    @inject_session
    async def create_endpoint(cls, session: AsyncSession) -> Endpoint:
        async with session.begin():
            new_endpoint = EndpointCreate()
            session.add(Endpoint(code=new_endpoint.code))

        return await cls.get_endpoint_by_code(new_endpoint.code)

    @classmethod
    @inject_session
    async def delete_by_code(
        cls,
        endpoint_code: str,
        session: AsyncSession
    ) -> None:
        async with session.begin():
            endpoint = await session.scalar(
                select(Endpoint).filter_by(code=endpoint_code)
            )
            await session.delete(endpoint)
