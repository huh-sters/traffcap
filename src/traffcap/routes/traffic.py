from fastapi import APIRouter, WebSocket
from traffcap.repositories import InboundRequestRepository
from traffcap.dto import InboundRequest
from traffcap.core import wait_for_notification
from websockets.exceptions import ConnectionClosed
from pydanja import DANJAResourceList


traffic_router = APIRouter(prefix="/traffic", tags=["Traffic"])


@traffic_router.get("/", response_model_exclude_none=True)
async def traffic_get() -> DANJAResourceList[InboundRequest]:
    """
    List all traffic
    """
    inbound_requests = await InboundRequestRepository.get_all_inbound_requests()

    # Convert from SQLAlchemy model to pydantic BaseModel

    return DANJAResourceList.from_basemodel_list(inbound_requests)


@traffic_router.websocket("/ws")
async def traffic_firehose(websocket: WebSocket):
    # TODO: Only send the newer requests instead of everything
    try:
        await websocket.accept()
        while True:
            inbound_requests = await InboundRequestRepository.get_all_inbound_requests()

            # Send more data
            if len(inbound_requests) > 0:
                response = DANJAResourceList.from_basemodel_list(inbound_requests)
                await websocket.send_text(response.model_dump_json())

            # Wait for an event from the message broker
            await wait_for_notification()

    except ConnectionClosed:
        pass
