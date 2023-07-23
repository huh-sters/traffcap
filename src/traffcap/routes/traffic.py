from fastapi import APIRouter, WebSocket
from fastapi.responses import Response
from pydantic_jsonapi import JsonApiModel
from traffcap.repositories import InboundRequestRepository
from traffcap.dto import InboundRequest
from traffcap.core import wait_for_notification
from websockets.exceptions import ConnectionClosed


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

@traffic_router.websocket("/ws")
async def traffic_firehose(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            inbound_requests = await InboundRequestRepository.get_all_inbound_requests()

            # Send more data
            response = InboundRequestList(
                data=[
                    InboundRequestList.resource_object(
                        id=inbound_request.id,
                        attributes=inbound_request
                    ) for inbound_request in inbound_requests
                ]
            )
            await websocket.send_text(response.json())

            # Wait for an event from the message broker
            await wait_for_notification()

    except ConnectionClosed:
        pass
