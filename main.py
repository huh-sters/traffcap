#!/usr/bin/env python3
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import api_routers
from starlette.exceptions import HTTPException
from starlette.requests import Request
from fastapi.responses import JSONResponse
"""
Application bootstrap
"""


app = FastAPI()

# Enable CORS from anywhere with anything
# TODO: Add UI to restrict these
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errors": [{
                "status": str(exc.status_code),
                "title": exc.detail
            }]
        }
    )


def main():
    """
    Add our routes to the application
    """
    assets_dir = Path("spa", "dist", "spa", "assets")

    # Static mount for SPA assets, with root files exposed elsewhere
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="spa")

    # API Routes
    for router in api_routers:
        app.include_router(router)


if __name__ in ["__main__", "main"]:
    main()
