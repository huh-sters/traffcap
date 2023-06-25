from fastapi import APIRouter, HTTPException
from pydantic_jsonapi import JsonApiModel
from traffcap.dto import (
    Endpoint,
    InboundRequest
)
from traffcap.repositories import EndpointRepository
"""
Endpoint management
"""

endpoint_router = APIRouter(prefix="/endpoints", tags=["Endpoints"])
EndpointRequest, EndpointResponse = JsonApiModel("endpoint", Endpoint)
_, EndpointResponseList = JsonApiModel("endpoint", Endpoint, list_response=True)
_, InboundRequestList = JsonApiModel("inbound_request", InboundRequest, list_response=True)


@endpoint_router.get("/")
async def endpoint_get() -> EndpointResponseList:  # type: ignore
    """
    Return a list of registered endpoints
    """
    endpoints = await EndpointRepository.get_all_endpoints()

    return EndpointResponseList(
        data=[
            EndpointResponseList.resource_object(
                id=endpoint.id,
                attributes=endpoint
            ) for endpoint in endpoints
        ]
    )


@endpoint_router.get("/{endpoint_code}")
async def endpoint_code_get(endpoint_code: str) -> EndpointResponse:  # type: ignore
    """
    Return a single registered endpoint
    """
    endpoint = await EndpointRepository.get_endpoint_by_code(endpoint_code)
    if not endpoint:
        raise HTTPException(404, detail="Endpoint not found")

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )


@endpoint_router.get("/{endpoint_code}/traffic")
async def get_endpoint_traffic(
    endpoint_code: str
) -> InboundRequestList:  # type: ignore
    """
    Return the traffic for this endpoint code
    """
    traffic = await EndpointRepository.get_endpoint_traffic(endpoint_code)

    return InboundRequestList(
        data=[
            InboundRequestList.resource_object(
                id=item.id,
                attributes=item
            ) for item in traffic
        ]
    )


@endpoint_router.post("/")
async def endpoint_create() -> EndpointResponse:  # type: ignore
    """
    Create a new endpoint
    """
    endpoint = await EndpointRepository.create_endpoint()

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )


@endpoint_router.delete("/{endpoint_code}")
async def endpoint_code_delete(endpoint_code: str) -> EndpointResponse:  # type: ignore
    """
    Delete an existing endpoint
    """
    endpoint = await EndpointRepository.get_endpoint_by_code(endpoint_code)
    if not endpoint:
        raise HTTPException(404, detail="Endpoint not found")

    await EndpointRepository.delete_by_code(endpoint_code)

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )
