import re
from fastapi import APIRouter, Request
from fastapi.responses import Response
from traffcap.config import settings
from traffcap.repositories import (
    InboundRequestRepository,
    RuleRepository
)
from traffcap.core import new_traffic_notification
from traffcap.model import HTTPVerbs
from traffcap.matches import rule_match
import json
"""
Inbound Requests
================

Deal with all inbound traffic from webhooks. This has a single route which works with all HTTP verbs.

"""

inbound_requests_router = APIRouter(
    prefix=f"/{settings.requests_prefix}",
    tags=["Requests"]
)


response_template = """
{
    "status": "{{method}} OK for {{endpoint_code}} with rule match: {{rule}}"
}
"""


@inbound_requests_router.api_route("/{endpoint_code}", methods=HTTPVerbs.to_list())
async def requests_route(endpoint_code: str, request: Request) -> Response:
    await InboundRequestRepository.store_request(endpoint_code, request)

    # Accept header can be a list of MIME types, we only react to the first
    accept_types = request.headers.get("accept", "").replace(" ", "").split(",")
    accept_types = list(filter(None, accept_types))

    if accept_types:
        content_type = accept_types[0]
    else:
        content_type = request.headers.get("content-type", "application/json")

    # Rule match usage
    rule_response = await rule_match(request)

    # Notify all listening web sockets
    new_traffic_notification()

    return rule_response
