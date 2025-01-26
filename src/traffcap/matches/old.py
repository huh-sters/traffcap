import re
from fastapi import Request
from enum import Enum
from abc import ABC, abstractmethod
from traffcap.config import settings
import asyncio


"""
Create AND/OR tree
"""

# Database storage
rules = [{
        "id": 1,
        "parent_id": None,
        "type": 0,  # Always True
        "pattern": "",
        "invert": False
    }, {
        "id": 2,
        "parent_id": 1,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 3,
        "parent_id": 1,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 4,
        "parent_id": 1,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 5,
        "parent_id": 2,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 6,
        "parent_id": 2,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 7,
        "parent_id": 2,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 8,
        "parent_id": 3,
        "type": 1,
        "pattern": "",
        "invert": False
    }, {
        "id": 9,
        "parent_id": 3,
        "type": 1,
        "pattern": "",
        "invert": False
    }
]



class RuleMatchException(Exception):
    pass


class RuleTypes(str, Enum):
    REQUEST_ENDPOINT = "EndpointRule"
    REQUEST_METHOD = "MethodRule"
    REQUEST_PROTOCOL = "ProtocolRule"
    REQUEST_DOMAIN_NAME = "DomainNameRule"
    REQUEST_PORT = "PortRule"
    REQUEST_HEADER_KEY = "HeaderKeyRule"
    REQUEST_HEADER_VALUE = "HeaderValueRule"
    REQUEST_HEADER_KEY_VALUE = "HeaderKeyValueRule"
    REQEUST_QUERY_PARAM_KEY = "QueryParamKeyRule"
    REQUEST_QUERY_PARAM_VALUE = "QueryParamValueRule"
    REQUEST_QUERY_PARAM_KEY_VALUE = "QueryParamKeyValueRule"
    REQUEST_BODY = "BodyRule"


class RuleMatch(ABC):
    def __init__(self, request: Request):
        self._request = request

    async def check_string(value: str, pattern: re.Pattern) -> bool:
        return pattern.search(value) is not None

    async def check_dictionary_keys(dictionary: dict, pattern: re.Pattern) -> bool:
        for key in dictionary:
            if pattern.search(key) is not None:
                return True
        
        return False

    async def check_dictionary_values(dictionary: dict, pattern: re.Pattern) -> bool:
        for key in dictionary:
            if pattern.search(dictionary[key]) is not None:
                return True
        
        return False

    async def check_dictionary_value(dictionary: dict, key: str, pattern: re.Pattern) -> bool:
        return pattern.search(dictionary.get(key, "")) is not None

    @abstractmethod
    async def check(self, key: str, pattern: str) -> bool:
        ...


class RootRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return True


class EndpointRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string(self._request.url.path, re.compile(fr"^/{settings.requests_prefix}/{pattern}"))


class MethodRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string(self._request.method, re.compile(pattern))


class ProtocolRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string(self._request.url.scheme, re.compile(pattern))


class DomainNameRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string(self._request.url.hostname, re.compile(pattern))


class PortRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string(str(self._request.url.port), re.compile(pattern))


class HeaderKeyRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_keys(self._request.headers, re.compile(pattern))


class HeaderValueRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_values(self._request.headers, re.compile(pattern))


class HeaderKeyValueRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_value(self._request.headers, key, re.compile(pattern))


class QueryParamKeyRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_keys(self._request.query_params, re.compile(pattern))


class QueryParamValueRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_values(self._request.query_params, re.compile(pattern))


class QueryParamKeyValueRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_dictionary_value(self._request.query_params, key, re.compile(pattern))


class BodyRule(RuleMatch):
    async def check(self, key: str, pattern: str) -> bool:
        return await self.check_string((await self._request.body()).decode("utf-8"), re.compile(pattern))


"""
Store the rule type in the database as an integer or as a string of the class name?
"""

async def rule_factory(rule_type: RuleTypes, request: Request) -> RuleMatch:
    g = globals()
    if rule_type.value not in g:
        raise RuleMatchException(f"Rule {rule_type.value} not found")
    
    return g[rule_type](request)


async def rule_match(request: Request) -> str:
    """
    Using the contents of the incoming request, match aspects and return
    a response.
    """
    return ""


async def main():
    a = Request({"type": "http"})
    keyed_rules = {}
    for rule in rules:  # Records from the database
        rule["children"] = []
        keyed_rules[rule["id"]] = rule

    root_rule = None

    for key in keyed_rules:
        if keyed_rules[key]["parent_id"]:
            keyed_rules[keyed_rules[key]["parent_id"]]["children"].append(keyed_rules[key])
        else:
            root_rule = keyed_rules[key]

    print(root_rule)

    # rule = await rule_factory(RuleTypes.REQEUST_QUERY_PARAM_KEY, a)
    # print(await rule.check("123", "123"))


if __name__ == "__main__":
    """
    Test this
    """
    asyncio.run(main())



# {
#     'id': 1, 
#     'parent_id': None, 
#     'type': 0, 
#     'pattern': '', 
#     'invert': False, 
#     'children': [{
#         'id': 2, 
#         'parent_id': 1, 
#         'type': 1, 
#         'pattern': '', 
#         'invert': False, 
#         'children': [{
#             'id': 5, 
#             'parent_id': 2, 
#             'type': 1, 
#             'pattern': '', 
#             'invert': False, 
#             'children': []
#         }, {
#             'id': 6, 
#             'parent_id': 2, 
#             'type': 1, 
#             'pattern': '', 
#             'invert': False, 
#             'children': []
#         }, {
#             'id': 7, 
#             'parent_id': 2, 
#             'type': 1, 
#             'pattern': '', 
#             'invert': False, 
#             'children': []
#         }]
#     }, {
#         'id': 3, 
#         'parent_id': 1, 
#         'type': 1, 
#         'pattern': '', 
#         'invert': False, 
#         'children': [{
#             'id': 8, 
#             'parent_id': 3, 
#             'type': 1, 
#             'pattern': '', 
#             'invert': False, 
#             'children': []
#         }, {
#             'id': 9, 
#             'parent_id': 3, 
#             'type': 1, 
#             'pattern': '', 
#             'invert': False, 
#             'children': []
#         }]
#     }, {
#         'id': 4, 
#         'parent_id': 1, 
#         'type': 1, 
#         'pattern': '', 
#         'invert': False, 
#         'children': []
#     }
# ]}


#!/usr/bin/env python3
from dataclasses import dataclass, field
from timeit import timeit
"""
Build an and/or tree from records and then playthrough

    A
   / \
  B   C
 / \
D   E

Vertical represents an AND, horizontal OR

In this example: A and (B or C) AND (D or E)

Nodes can have any number of children

  A
 /|\
B C D

Equates to: A and (B or C or D)

We need to build a tree from records. Each record with a parent.

Need to figure out how to edit the operations in UI for this to make sense

This also excludes inversion of node values
"""
@dataclass
class Node:
    node_id: int | None = None
    parent_id: int | None = None
    operation: bool | None = None
    children: list["Node"] = field(default_factory=list)

# Record structure
nodes = [
    {"node_id": 1, "parent_id": None, "operation": True},  # Root

    {"node_id": 2, "parent_id": 1, "operation": True},  # First level, same parent, these are OR'd together
    {"node_id": 3, "parent_id": 1, "operation": False},
    {"node_id": 4, "parent_id": 1, "operation": False},

    {"node_id": 5, "parent_id": 2, "operation": False},  # Second level, same parent, these are OR'd together
    {"node_id": 6, "parent_id": 2, "operation": True},

    {"node_id": 7, "parent_id": 3, "operation": True},  # Second level, same parent, these are OR'd together
    {"node_id": 8, "parent_id": 3, "operation": True},
    {"node_id": 9, "parent_id": 3, "operation": True}
]

# Append all nodes to the tree
tree_nodes = {}
for node in nodes:  # O(n)
    tree_nodes[node["node_id"]] = Node(**node)

root = None

# Attach all nodes to parents
for key in tree_nodes:  # O(n)
    if tree_nodes[key].parent_id:
        tree_nodes[tree_nodes[key].parent_id].children.append(tree_nodes[key])
    else:
        # Found the root node
        root = tree_nodes[key]


def calculate_node_value(node: Node) -> bool:  # DFS, O(|V|+|E|) wcs
    """
    DFS on the AND/OR tree
    Recursive function to calculate the total tree value. If there are no
    children, then return the value of the node. Otherwise, or the results
    of the children together, then AND with the current node
    """
    if not node.children:
        return node.operation

    child_result = False
    for child in node.children:
        child_result = child_result or calculate_node_value(child)

    return node.operation and child_result

print(calculate_node_value(root))