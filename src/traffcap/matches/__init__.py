from fastapi import Request
from traffcap.matches.rules import *
from traffcap.repositories import RuleRepository
from traffcap.model import Match
"""
Rule matching using an AND/OR tree:

  P <- Child results are AND'd with the parent value
 /|\
A B C <- Children values are OR'd together


A RootRule is a pseudo node in the tree that always returns true.
This is a shortcut to providing trees that can do operations like
A or B or C
These three are then child nodes of this pseudo node which are AND'd
with the result from here. This means that our AND/OR tree can
represent AND operations with edges all child nodes being OR'd together.

NOT's are applied directly to the node value, not to a group of child nodes.

This provides us with O(|V|+|E|) using DFS while trying to calculate the value
of the tree.
"""


class RuleMatchException(Exception):
    pass


async def rule_factory(rule_type: str, request: Request, key: str, pattern: str, parent_id: int, invert: bool) -> RuleMatch:
    g = globals()
    if rule_type not in g:
        raise RuleMatchException(f"Rule {rule_type} not found")
    
    return g[rule_type](request=request, key=key, pattern=pattern, parent_id=parent_id, invert=invert)


async def calculate_node_value(rule: RuleMatch) -> bool:
    """
    DFS to calculate the total tree value. If there are no
    children, then return the value of the node. Otherwise, or the results
    of the children together, then AND with the current node
    """
    result = await rule.check()
    if rule.invert:
        result = not result

    if not rule.children:
        return result

    child_result = False
    for child in rule.children:
        child_result = child_result or await calculate_node_value(child)

    return result and child_result


async def add_rules() -> None:
    """
    Add our test rules to the database
    """
    lowest = await RuleRepository.get_lowest_priority()
    rule = await RuleRepository.create_rule(name="Test rule", priority=lowest + 1, content_type="application/json", template="<h1>Hello</h1>")
    root_match = await RuleRepository.add_match(Match(rule_id=rule.id, parent_id=None, match_type="RootRule", key=None, pattern="", invert=False))
    method_match = await RuleRepository.add_match(Match(rule_id=rule.id, parent_id=root_match.id, match_type="MethodRule", key=None, pattern="GET", invert=False))
    endpoint_match = await RuleRepository.add_match(Match(rule_id=rule.id, parent_id=method_match.id, match_type="EndpointRule", key=None, pattern="f67c66f43a9648d0ba83df7bf1e36907", invert=False))
    header_match = await RuleRepository.add_match(Match(rule_id=rule.id, parent_id=endpoint_match.id, match_type="HeaderKeyValueRule", key="accept", pattern="application/json", invert=False))

async def rule_match(request: Request) -> str:
    """
    Scan through all the decision trees until we find a match
    We should be able to improve this by collecting stats and
    re-ordering the trees to the most matched first.
    """
    await RuleRepository.clear_all_rules()
    await add_rules()
    test_rules = await RuleRepository.get_all_rules_by_priority()
    for rule in test_rules:
        keyed_matches = {}
        for match in rule.matches:
            keyed_matches[match.id] = await rule_factory(
                rule_type=match.match_type,
                request=request,
                key=match.key,
                pattern=match.pattern,
                parent_id=match.parent_id,
                invert=match.invert
            )

        root_rule = None

        for key in keyed_matches:
            if keyed_matches[key].parent_id:
                keyed_matches[keyed_matches[key].parent_id].children.append(keyed_matches[key])
            else:
                root_rule = keyed_matches[key]

        result = await calculate_node_value(root_rule)
        if result:  # Found a match, send the response
            return rule.template

    return {"match": False}
