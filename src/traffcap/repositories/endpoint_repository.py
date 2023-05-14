from typing import List
from .repository import Repository
from traffcap.model import Endpoint
from traffcap.dto import EndpointCreate
from sqlalchemy import select
from uuid import uuid4


class EndpointRepository(Repository):
    @classmethod
    async def add_endpoint(cls, endpoint: EndpointCreate) -> Endpoint:
        async with cls.session() as session:
            session.add(Endpoint(**endpoint.dict()))
            session.commit()

    @classmethod
    async def get_endpoint_by_id(cls, endpoint_id: int) -> Endpoint:
        async with cls.session() as session:
            return session.get(Endpoint, endpoint_id)

    @classmethod
    async def get_all_endpoints(cls) -> List[Endpoint]:
        async with cls.session() as session:
            return session.query(Endpoint).all()

    @classmethod
    async def get_endpoint_by_code(cls, endpoint_code:str) -> Endpoint:
        async with cls.session() as session:
            return session.scalar(
                select(Endpoint).filter_by(code=endpoint_code)
            )

    @classmethod
    async def create_endpoint(cls) -> Endpoint:
        async with cls.session() as session:
            new_code = uuid4().hex
            session.add(Endpoint(code=new_code))
            session.commit()

        return cls.get_endpoint_by_code(new_code)

    @classmethod
    async def delete_by_code(cls, endpoint_code: str) -> None:
        async with cls.session() as session:
            session.delete(session.scalar(
                select(Endpoint).filter_by(code=endpoint_code)
            ))
            session.commit()
