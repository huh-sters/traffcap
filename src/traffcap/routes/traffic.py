from fastapi import APIRouter, WebSocket
from fastapi.responses import Response
from pydantic_jsonapi import JsonApiModel
from traffcap.repositories import (
    InboundRequestRepository
)
from traffcap.dto import InboundRequest
from asyncio import sleep
from traffcap.core import store
import logging


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
    await websocket.accept()
    while True:
        last_message = store.get("last_message", 0)

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
        while last_message == store.get("last_message", 0):
            await sleep(0.5)

        logging.info("Received an event, refreshing...")
