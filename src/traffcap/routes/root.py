from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, Response
from traffcap.config import settings
from fastapi.templating import Jinja2Templates
"""
Files in the root directory
If a frontend path is set in environment variables, use it here
"""

root_router = APIRouter(include_in_schema=False)
dist = Path(str(Path(__file__).parent.parent), "spa", "dist", "spa")
if settings.frontend_path:
    dist = settings.frontend_path


template_dir = Path(str(Path(__file__).parent.parent), "templates")
templates = Jinja2Templates(directory=template_dir)


@root_router.get("/")
async def root_get() -> HTMLResponse:
    with open(dist / "index.html", "r") as index_handle:
        index = index_handle.read()

    return HTMLResponse(index)


@root_router.get("/favicon.ico")
async def favicon_get() -> FileResponse:
    return FileResponse(dist / "favicon.ico")


@root_router.get("/env.js")
async def environment_get(request: Request) -> Response:
    """
    Server URL injection for the frontend. We can then pre-build the SPA
    in Quasar.
    """
    return templates.TemplateResponse(
        name="env.js",
        context={
            "request": request,
            "server_url": settings.server_url,
            "websocket_protocol": settings.websocket_protocol,
            "http_protocol": settings.http_protocol
        },
        status_code=200,
        media_type="application/javascript"
    )
