from pathlib import Path
from importlib import import_module
from fastapi import APIRouter
"""
For each Python file in this package, locate the APIRouter variable
"""


__all__ = [
    "api_routers"
]

api_routers = []

for entry in Path(__path__[0]).iterdir():
    """
    Auto-build the list of available routers in this package
    """
    if (
        entry.name == "__init__.py" or
        not entry.is_file() or
        not entry.name.endswith(".py")
    ):
        continue

    import_module(f".{entry.stem}", "routes")
    for local in locals()[entry.stem].__dict__:
        instance = getattr(locals()[entry.stem], local)
        if isinstance(instance, APIRouter):
            api_routers.append(instance)
