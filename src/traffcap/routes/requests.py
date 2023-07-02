import re
from fastapi import APIRouter, Request
from fastapi.responses import Response
from traffcap.config import settings
from traffcap.repositories import InboundRequestRepository
from traffcap.repositories import RuleRepository
from traffcap.dto import HTTPVerbs
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


response_template = """
{
    "status": "{{method}} OK for {{endpoint_code}} with rule match: {{rule}}"
}
"""


@requests_router.api_route("/{endpoint_code}", methods=HTTPVerbs.to_list())
async def requests_route(endpoint_code: str, request: Request) -> Response:
    await InboundRequestRepository.store_request(endpoint_code, request)

    # Accept header can be a list of MIME types, we only react to the first
    # accept_types = request.headers.get("accept", "").replace(" ", "").split(",")
    # accept_types = list(filter(None, accept_types))

    # if accept_types:
    #     return_type = accept_types[0]
    # else:
    #     return_type = request.headers.get("content-type", "application/json")

    # Calculate the response to give
    rules = await RuleRepository.get_all_rules()
    for rule in rules:
        if re.fullmatch(rule.rule, endpoint_code):
            """
            Found a match
            * run the actions
            * send the response
            TODO: Actions go here
            TODO: Response goes here. It should reflect the requested content type
            1. If there's an accept header, use that
            2. If there's a content-type, use that to match what was sent
            3. Default to application/json
            """
            return Response({
                "status": f"{request.method} OK for {endpoint_code} with rule match: {rule.rule}"
            })

    # TODO: Default response
    return Response({
        "status": f"{request.method} OK for {endpoint_code}"
    })
