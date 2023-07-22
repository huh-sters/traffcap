from .rules import rule_router
from .inbound_requests import inbound_requests_router
from .root import root_router
from .traffic import traffic_router
"""
For each Python file in this package, locate the APIRouter variable
"""


__all__ = [
    "api_routers"
]

api_routers = [
    root_router,
    inbound_requests_router,
    rule_router,
    traffic_router
]
