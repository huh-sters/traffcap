from fastapi import APIRouter, HTTPException
from pydantic_jsonapi import JsonApiModel
from dto import Endpoint
from repositories import EndpointRepository
"""
Endpoint management
"""

endpoint_router = APIRouter(prefix="/endpoints", tags=["Endpoints"])
EndpointRequest, EndpointResponse = JsonApiModel("endpoint", Endpoint)
_, EndpointResponseList = JsonApiModel("endpoint", Endpoint, list_response=True)


@endpoint_router.get("/")
async def endpoint_get() -> EndpointResponseList:
    """
    Return a list of registered endpoints
    """
    endpoints = EndpointRepository.get_all_endpoints()

    return EndpointResponseList(
        data=[
            EndpointResponseList.resource_object(
                id=endpoint.id,
                attributes=endpoint
            ) for endpoint in endpoints]
    )


@endpoint_router.get("/{endpoint_code}")
async def endpoint_code_get(endpoint_code: str) -> EndpointResponse:
    """
    Return a single registered endpoint
    """
    endpoint = EndpointRepository.get_endpoint_by_code(endpoint_code)
    if not endpoint:
        raise HTTPException(404, detail="Endpoint not found")

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )


@endpoint_router.post("/")
async def endpoint_create() -> EndpointResponse:
    """
    Create a new endpoint
    """
    endpoint = EndpointRepository.create_endpoint()

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )


@endpoint_router.delete("/{endpoint_code}")
async def endpoint_code_delete(endpoint_code: str) -> EndpointResponse:
    """
    Delete an existing endpoint
    """
    endpoint = EndpointRepository.get_endpoint_by_code(endpoint_code)
    if not endpoint:
        raise HTTPException(404, detail="Endpoint not found")

    EndpointRepository.delete_by_code(endpoint_code)

    return EndpointResponse(
        data=EndpointResponse.resource_object(
            id=endpoint.id,
            attributes=endpoint
        )
    )
