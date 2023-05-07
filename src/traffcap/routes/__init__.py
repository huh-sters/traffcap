from pathlib import Path
from fastapi import APIRouter
from .endpoints import endpoint_router
from .requests import requests_router
from .root import root_router
"""
For each Python file in this package, locate the APIRouter variable
"""


__all__ = [
    "api_routers"
]

api_routers = [
    root_router,
    requests_router,
    endpoint_router
]
