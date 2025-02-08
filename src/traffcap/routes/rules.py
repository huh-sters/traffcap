from fastapi import APIRouter, HTTPException
from pydanja import DANJAResourceList, DANJAResource, DANJAErrorList
from traffcap.model.response import RuleMatches
from traffcap.repositories import RuleRepository
from typing import Union
"""
Endpoint management
"""

rule_router = APIRouter(prefix="/rule", tags=["Rules"])


@rule_router.get("/", response_model_exclude_none=True)
async def rule_get() -> DANJAResourceList[RuleMatches]:
    """
    Return a list of rules
    TODO: Support rule list paging
    """
    rules = await RuleRepository.get_all_rules()

    return DANJAResourceList.from_basemodel_list(list(rules))


@rule_router.get("/{rule_id}")
async def rule_get_by_id(rule_id: int) -> Union[DANJAResource[RuleMatches], DANJAErrorList]:
    """
    Return a single rule
    """
    rule = await RuleRepository.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(404, detail="Rule not found")

    return DANJAResource.from_basemodel(rule)
