from fastapi import APIRouter, HTTPException, Request
from pydantic_jsonapi import JsonApiModel
from traffcap.dto import (
    Rule,
    RuleCreate,
    InboundRequest
)
from traffcap.repositories import RuleRepository
from pydantic.error_wrappers import ValidationError
from typing import List
"""
Endpoint management
"""

rule_router = APIRouter(prefix="/rules", tags=["Rules"])
RuleRequest, RuleResponse = JsonApiModel("rule", Rule)
RuleCreateRequest, _ = JsonApiModel("rule", RuleCreate)
_, RuleResponseList = JsonApiModel("rule", Rule, list_response=True)
_, InboundRequestList = JsonApiModel("inbound_request", InboundRequest, list_response=True)


def friendly_validation_error(ve: ValidationError) -> List[str]:
    return [f"{'/'.join(e['loc'])} - {e['msg']}" for e in ve.errors()]


@rule_router.get("/")
async def rule_get() -> RuleResponseList:  # type: ignore
    """
    Return a list of rules
    TODO: Support paging
    """
    rules = await RuleRepository.get_all_rules()

    return RuleResponseList(
        data=[
            RuleResponseList.resource_object(
                id=rule.id,
                attributes=rule
            ) for rule in rules
        ]
    )


@rule_router.get("/{rule_id}")
async def rule_get_by_id(rule_id: int) -> RuleResponse:  # type: ignore
    """
    Return a single rule
    """
    rule = await RuleRepository.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")

    return RuleResponse(
        data=RuleResponse.resource_object(
            id=rule.id,
            attributes=rule
        )
    )


@rule_router.post("/")
async def rule_create(request: Request) -> RuleResponse:  # type: ignore
    """
    Create a new rule
    * Check that it doesn't clash with another rule

    While it is possible to find an empty intersect between two regex patterns, it
    would be costly to perform it here. Instead, we just perform an exact string
    match across the rules table.
    """
    try:
        # Validate the inbound payload
        payload = RuleCreateRequest(**(await request.json()))

        # See if the rule is already there
        rules = await RuleRepository.find_matching_rules(
            rule=payload.data.attributes.rule
        )
        if len(rules.all()) > 0:
            raise HTTPException(
                400,
                detail=f"Rule {payload.data.attributes.rule!r} already exists"
            )

        # Create the new rule
        new_rule = await RuleRepository.create_rule(
            rule=payload.data.attributes.rule
        )

        return RuleResponse(
            data=RuleResponse.resource_object(
                id=new_rule.id,
                attributes=new_rule
            )
        )
    except ValidationError as ve:
        raise HTTPException(
            400,
            detail=friendly_validation_error(ve)
        )


@rule_router.delete("/{rule_id}")
async def rule_delete_by_id(rule_id: int) -> RuleResponse:  # type: ignore
    """
    Delete an existing rule
    """
    rule = await RuleRepository.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")

    await RuleRepository.delete_rule_by_id(rule_id)

    return RuleResponse(
        data=RuleResponse.resource_object(
            id=rule.id,
            attributes=rule
        )
    )
