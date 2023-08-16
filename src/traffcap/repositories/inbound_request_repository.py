from .repository import Repository
from fastapi import Request
from traffcap.dto import InboundRequestCreate, InboundRequest
from traffcap.model import InboundRequestModel
from sqlalchemy import select
from typing import List


class InboundRequestRepository(Repository):
    @classmethod
    async def store_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> None:
        """
        Store the components of the request
        """
        async with cls.session() as session:
            async with session.begin():
                new_inbound_request = await InboundRequestCreate.from_request(
                    endpoint_code,
                    request
                )
                session.add(InboundRequestModel(
                    endpoint_code=endpoint_code,
                    method=new_inbound_request.method,
                    headers=new_inbound_request.headers,
                    query_params=new_inbound_request.query_params,
                    body=new_inbound_request.body
                ))

    @classmethod
    async def get_all_inbound_requests(cls) -> List[InboundRequest]:
        requests = []
        async with cls.session() as session:
            results = await session.scalars(select(InboundRequestModel).order_by(InboundRequestModel.id.desc()))
            for request in results.all():
                requests.append(InboundRequest.model_validate(request, from_attributes=True))

        return requests
