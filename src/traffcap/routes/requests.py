from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from traffcap.config import settings
from traffcap.repositories import InboundRequestRepository
from traffcap.dto import HTTPVerbs
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


@requests_router.api_route("/{endpoint_code}", methods=HTTPVerbs.to_list())
async def requests_route(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(endpoint_code, request)

    return JSONResponse({
        "status": f"{request.method} OK for {endpoint_code}"
    })
