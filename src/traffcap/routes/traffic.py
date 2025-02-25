import logging
import json
from fastapi import APIRouter, WebSocket
from fastapi.routing import serialize_response
from fastapi.utils import create_model_field
from traffcap.repositories import InboundRequestRepository
from traffcap.model.response import InboundRequestHeadersQueryParams
from traffcap.core import wait_for_notification
from websockets.exceptions import ConnectionClosed
from starlette.websockets import WebSocketDisconnect
from pydanja import DANJAResourceList, DANJASingleResource
from asyncio import sleep
from typing import Optional


traffic_router = APIRouter(prefix="/traffic", tags=["Traffic"])


@traffic_router.get("/", response_model_exclude_none=True)
async def traffic_get() -> DANJAResourceList[InboundRequestHeadersQueryParams]:
    """
    List all traffic
    """
    inbound_requests = await InboundRequestRepository.get_all_inbound_requests()
    return DANJAResourceList.from_basemodel_list(list(inbound_requests))


@traffic_router.websocket("/ws")
@traffic_router.websocket("/ws/{page}/{page_size}")
async def traffic_firehose(websocket: WebSocket, page: Optional[int] = 0, page_size: Optional[int] = 10):
    # TODO: Only send the newer requests instead of everything in the WebSocket
    field_model = create_model_field(
        name="response_model",
        type_=DANJAResourceList[InboundRequestHeadersQueryParams],
        mode="serialization"
    )
    try:
        await websocket.accept()
        while True:
            inbound_requests = await InboundRequestRepository.get_inbound_requests_by_page(page_size, page)
            request_count = await InboundRequestRepository.get_inbound_request_count()
            # Send more data
            if len(inbound_requests) > 0:
                response = DANJAResourceList.from_basemodel_list(list(inbound_requests))
                response.include_from_basemodels(list())
                response.included = [(DANJASingleResource(
                    type="pagination",
                    attributes={
                        "page": page,
                        "count": request_count
                    }
                ))]
                # Serialise to the target response model
                await websocket.send_text(json.dumps(
                    await serialize_response(
                        field=field_model,
                        response_content=response,
                        exclude_none=True
                    )
                ))

            # Wait for an event from the message broker
            async for _ in wait_for_notification():
                # Check the connection
                await sleep(0.5)
                # TODO: Figure out how to check websocket connections without the ping
                await websocket.send_text("ping")

    except (ConnectionClosed, WebSocketDisconnect):
        # Keep on truckin'
        logging.debug("Websocket disconnected")
    except Exception as ex:
        logging.error(ex)
