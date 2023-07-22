from fastapi import APIRouter
from fastapi.responses import Response
from pydantic_jsonapi import JsonApiModel
from traffcap.repositories import (
    InboundRequestRepository
)
from traffcap.dto import InboundRequest


traffic_router = APIRouter(prefix="/traffic", tags=["Traffic"])
_, InboundRequestList = JsonApiModel("inbound_request", InboundRequest, list_response=True)


@traffic_router.get("/")
async def traffic_get() -> Response:
    """
    List all traffic
    """
    inbound_requests = await InboundRequestRepository.get_all_inbound_requests()

    return InboundRequestList(
        data=[
            InboundRequestList.resource_object(
                id=inbound_request.id,
                attributes=inbound_request
            ) for inbound_request in inbound_requests
        ]
    )
