from fastapi import APIRouter, HTTPException
from pydanja import DANJAResourceList, DANJAResource, DANJAErrorList
from traffcap.model import Rule
from traffcap.repositories import RuleRepository
from pydantic import ValidationError
from typing import Union
"""
Endpoint management
"""

rule_router = APIRouter(prefix="/rules", tags=["Rules"])


def friendly_validation_error(ve: ValidationError) -> list[str]:
    return [
        f"{'/'.join(str(element) for element in e['loc'])} - {e['msg']}"
        for e in ve.errors()
    ]


@rule_router.get("/")
async def rule_get() -> DANJAResourceList[Rule]:
    """
    Return a list of rules
    TODO: Support rule list paging
    """
    rules = await RuleRepository.get_all_rules()

    return DANJAResourceList.from_basemodel_list(list(rules))


@rule_router.get("/{rule_id}")
async def rule_get_by_id(rule_id: int) -> Union[DANJAResource[Rule], DANJAErrorList]:
    """
    Return a single rule
    """
    rule = await RuleRepository.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")

    return DANJAResource.from_basemodel(rule)


# @rule_router.post("/")
# async def rule_create(payload: DANJAResource[Rule]) -> Union[DANJAResource[Rule], DANJAErrorList]:
#     """
#     Create a new rule
#     * Check that it doesn't clash with another rule

#     While it is possible to find an empty intersect between two regex patterns, it
#     would be costly to perform it here. Instead, we just perform an exact string
#     match across the rules table.
#     """
#     try:
#         # See if the rule is already there
#         rules = await RuleRepository.find_matching_rules(
#             rule=payload.data.attributes.rule
#         )
#         if len(rules) > 0:
#             raise HTTPException(
#                 400,
#                 detail=f"Rule {payload.data.attributes.rule!r} already exists"
#             )

#         # Create the new rule
#         new_rule = await RuleRepository.create_rule(
#             rule=payload.data.attributes.rule
#         )

#         if not new_rule:
#             raise HTTPException(
#                 400,
#                 detail=f"Unable to create rule for {payload.data.attributes.rule}"
#             )

#         return DANJAResource.from_basemodel(new_rule)
#     except ValidationError as ve:
#         raise HTTPException(
#             400,
#             detail=friendly_validation_error(ve)
#         )


@rule_router.delete("/{rule_id}")
async def rule_delete_by_id(rule_id: int) -> DANJAResource[Rule]:
    """
    Delete an existing rule
    """
    rule = await RuleRepository.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")

    await RuleRepository.delete_rule_by_id(rule_id)

    return DANJAResource.from_basemodel(rule)
