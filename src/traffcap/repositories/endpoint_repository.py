from typing import Optional
from .repository import (
    Repository,
    inject_session
)
from traffcap.dto import EndpointCreate
from traffcap.model import Endpoint
from sqlalchemy import select, ScalarResult
from uuid import uuid4
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
    async def create_endpoint(cls, session: AsyncSession) -> Endpoint:
        async with session.begin():
            new_code = uuid4().hex
            new_endpoint = EndpointCreate(code=new_code)
            session.add(new_endpoint)
            # session.add(Endpoint(code=new_code))

        return await cls.get_endpoint_by_code(new_code)

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
