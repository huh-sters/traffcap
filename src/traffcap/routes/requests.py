import re
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from traffcap.config import settings
from traffcap.repositories import InboundRequestRepository
from traffcap.repositories import RuleRepository
from traffcap.dto import HTTPVerbs
"""
Files in the root directory
"""

requests_router = APIRouter(prefix=f"/{settings.requests_prefix}", tags=["Requests"])


@requests_router.api_route("/{endpoint_code}", methods=HTTPVerbs.to_list())
async def requests_route(endpoint_code: str, request: Request) -> JSONResponse:
    await InboundRequestRepository.store_request(endpoint_code, request)

    # Calculate the response to give
    rules = await RuleRepository.get_all_rules()
    for rule in rules:
        if re.fullmatch(rule.rule, endpoint_code):
            """
            Found a match
            * run the actions
            * send the response
            """
            # TODO: Actions go here
            # TODO: Response goes here. It should reflect the requested content type
            return JSONResponse({
                "status": f"{request.method} OK for {endpoint_code} with rule match: {rule.rule}"
            })

    # TODO: Default response
    return JSONResponse({
        "status": f"{request.method} OK for {endpoint_code}"
    })
