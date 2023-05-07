import logging
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from traffcap.config import settings
"""
Files in the root directory
If a frontend path is set in environment variables, use it here
"""

root_router = APIRouter(include_in_schema=False)
dist = Path(str(Path(__file__).parent.parent), "spa", "dist", "spa")
if settings.frontend_path:
    dist = settings.frontend_path


@root_router.get("/")
async def root_get() -> HTMLResponse:
    with open(dist / "index.html", "r") as index_handle:
        index = index_handle.read()

    return HTMLResponse(index)


@root_router.get("/favicon.ico")
async def favicon_get() -> FileResponse:
    return FileResponse(dist / "favicon.ico")
