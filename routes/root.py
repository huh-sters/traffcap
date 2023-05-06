from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
"""
Files in the root directory
"""

root_router = APIRouter(include_in_schema=False)
DIST = Path("spa", "dist", "spa")


@root_router.get("/")
async def root_get() -> HTMLResponse:
    with open(DIST / "index.html", "r") as index_handle:
        index = index_handle.read()

    return HTMLResponse(index)


@root_router.get("/favicon.ico")
async def favicon_get() -> FileResponse:
    return FileResponse(DIST / "favicon.ico")
