from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from traffcap.config import settings
from traffcap.repositories import InboundRequestRepository
from traffcap.dto import HTTPVerbs
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


async def calculate_response(endpoint_code: str, method: HTTPVerbs) -> JSONResponse:
    return JSONResponse({
        "status": f"{method} OK for {endpoint_code}"
    })


@requests_router.get("/{endpoint_code}")
async def requests_get(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )
    """
    Send a response:
    * Match the endpoint_code with a regex match rule
    * If it matches, send the respons from the rule
    * Otherwise, send the default response
    """
    return await calculate_response(endpoint_code, request.method)


@requests_router.post("/{endpoint_code}")
async def requests_post(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.put("/{endpoint_code}")
async def requests_put(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.patch("/{endpoint_code}")
async def requests_patch(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.delete("/{endpoint_code}")
async def requests_delete(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.options("/{endpoint_code}")
async def requests_options(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.head("/{endpoint_code}")
async def requests_head(endpoint_code: str, request: Request) -> JSONResponse:
    """
    There will be no body returned by this
    """
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)


@requests_router.trace("/{endpoint_code}")
async def requests_trace(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(
        endpoint_code,
        request.method,
        request
    )

    return await calculate_response(endpoint_code, request.method)
