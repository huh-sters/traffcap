from .repository import Repository
from fastapi import Request
from traffcap.dto import InboundRequestCreate
from traffcap.model import InboundRequest


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
        session = await cls.new_session()
        async with session.begin():
            new_inbound_request = await InboundRequestCreate.from_request(
                endpoint_code,
                request
            )
            session.add(InboundRequest(
                endpoint_code=endpoint_code,
                method=new_inbound_request.method,
                headers=new_inbound_request.headers,
                query_params=new_inbound_request.query_params,
                body=new_inbound_request.body
            ))
