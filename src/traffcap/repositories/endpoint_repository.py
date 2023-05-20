from typing import List
from .repository import Repository
from traffcap.model import Endpoint
from sqlalchemy import select
from uuid import uuid4


class EndpointRepository(Repository):
    @classmethod
    async def get_endpoint_by_id(cls, endpoint_id: int) -> Endpoint:
        async with cls.session() as session:
            return await session.get(Endpoint, endpoint_id)

    @classmethod
    async def get_all_endpoints(cls) -> List[Endpoint]:
        async with cls.session() as session:
            results = await session.scalars(select(Endpoint))
            return results

    @classmethod
    async def get_endpoint_by_code(cls, endpoint_code:str) -> Endpoint:
        async with cls.session() as session:
            return await session.scalar(
                select(Endpoint).filter_by(code=endpoint_code)
            )

    @classmethod
    async def create_endpoint(cls) -> Endpoint:
        async with cls.session() as session:
            async with session.begin():
                new_code = uuid4().hex
                session.add(Endpoint(code=new_code))

        return await cls.get_endpoint_by_code(new_code)

    @classmethod
    async def delete_by_code(cls, endpoint_code: str) -> None:
        async with cls.session() as session:
            async with session.begin():
                endpoint = await session.scalar(
                    select(Endpoint).filter_by(code=endpoint_code)
                )
                await session.delete(endpoint)
