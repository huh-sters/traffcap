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
            new_inbound_request = await InboundRequestCreate.from_request(
                endpoint_code,
                request
            )
            session.add(InboundRequestModel(**new_inbound_request.model_dump()))
            await session.commit()

    @classmethod
    async def get_all_inbound_requests(cls) -> List[InboundRequest]:
        """
        TODO: Reduce the double handling of models
        Can we reduce the double handling of models between sqlalchemy and
        pydantic? It would be nice to pass the select statement to the scalars()
        method along with some kind of builder that generates pydantic models directly
        """
        requests = []
        async with cls.session() as session:
            results = await session.scalars(
                select(InboundRequestModel)
                    .order_by(InboundRequestModel.id.desc())
            )
            for request in results.all():
                requests.append(
                    InboundRequest.model_validate(request, from_attributes=True)
                )

        return requests
