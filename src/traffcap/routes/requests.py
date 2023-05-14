from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from traffcap.config import settings
from starlette.datastructures import Headers, QueryParams
from traffcap.repositories import InboundRequestRepository
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


@requests_router.get("/{endpoint_code}")
async def requests_get(endpoint_code: str, request: Request) -> JSONResponse:
    """
    Is this request endpoint code in our database?
    Setting to only accept endpoint codes previously registered (strict)
    Otherwise record all endpoint codes
    Responses will be customizable

    headers
    query_params
    cookies
    body
    called url
    client
    scope
    session
    state
    url
    user

    Do we store these as individual fields or as a serialisation?
    """
    # Headers are a key-value pair
    # Now create a new Headers object by serializing and de-serializing the object
    # json_headers = json.dumps(jsonable_encoder(request.headers))
    # This has been serialized, now create one from whole-cloth
    # dict_headers = json.loads(json_headers)
    # new_headers = Headers(headers=dict_headers)
    # How do we get a set of cookies from this?

    # Query params are a dictionary?
    # json_query = json.dumps(jsonable_encoder(request.query_params))
    # Potentially the same
    # dict_query = json.loads(json_query)
    # new_query = QueryParams(dict_query)

    # Body
    # body = await request.body()  # Handle the body based on content type
    # json_body = await request.json()

    # At this stage we have the raw aspects of the request as strings
    # Store them...
    await InboundRequestRepository.upgrade()
    await InboundRequestRepository.store_request(endpoint_code, request)

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
