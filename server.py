#!/usr/bin/env python3
from pathlib import Path
import click
from typing import Any
from gunicorn.app.base import BaseApplication
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


"""
Direct CLI support
"""


# Class for running FastAPI from within Python itself
class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Any:
        return self.application


@click.command()
@click.option(
    "--workers",
    default=4,
    show_default=True,
    type=int,
    help="Number of Uvicorn workers to use"
)
@click.option(
    "--bind",
    default="127.0.0.1",
    show_default=True,
    type=str,
    help="Interface to bind the server to"
)
@click.option(
    "--port",
    default="9669",
    show_default=True,
    type=str,
    help="Port to use"
)
def cli(workers: int, bind: str, port: str) -> None:
    """
    Start gunicorn with uvicorn workers
    """
    options = {
        "bind": f"{bind}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
    }
    # Attach our routes
    main()
    # Run the application
    StandaloneApplication(app, options).run()


if __name__ in ["__main__", "server"]:
    main()
