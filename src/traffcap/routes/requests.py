from fastapi import APIRouter
from fastapi.responses import JSONResponse
from traffcap.config import settings
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


@requests_router.get("/{endpoint_code}")
async def requests_get(endpoint_code: str) -> JSONResponse:
    """
    Is this request endpoint code in our database?
    Setting to only accept endpoint codes previously registered (strict)
    Otherwise record all endpoint codes
    Responses will be customizable
    """
    return JSONResponse({
        "status": f"GET OK for {endpoint_code}"
    })


@requests_router.post("/{endpoint_code}")
async def requests_post(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"POST OK for {endpoint_code}"
    })


@requests_router.put("/{endpoint_code}")
async def requests_put(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"PUT OK for {endpoint_code}"
    })


@requests_router.patch("/{endpoint_code}")
async def requests_patch(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"PATCH OK for {endpoint_code}"
    })


@requests_router.delete("/{endpoint_code}")
async def requests_delete(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"DELETE OK for {endpoint_code}"
    })


@requests_router.options("/{endpoint_code}")
async def requests_options(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"OPTIONS OK for {endpoint_code}"
    })


@requests_router.head("/{endpoint_code}")
async def requests_head(endpoint_code: str) -> JSONResponse:
    """
    There will be no body returned by this
    """
    return JSONResponse({
        "status": f"HEAD OK for {endpoint_code}"
    })


@requests_router.trace("/{endpoint_code}")
async def requests_trace(endpoint_code: str) -> JSONResponse:
    return JSONResponse({
        "status": f"TRACE OK for {endpoint_code}"
    })
