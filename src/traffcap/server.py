#!/usr/bin/env python3
from pathlib import Path
import click
import logging
from traffcap.core import (
    banner,
    log_setup,
    StandaloneApplication,
    start_store
)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from traffcap.routes import api_routers
from starlette.exceptions import HTTPException
from starlette.requests import Request
from fastapi.responses import JSONResponse
from traffcap.repositories import Repository
from fastapi.openapi.utils import get_openapi
from pydanja import danja_openapi
"""
Application bootstrap
"""


start_store()

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI",
        version="2.5.0",
        summary="FastAPI",
        description="FastAPI",
        routes=app.routes,
    )

    app.openapi_schema = danja_openapi(openapi_schema)

    return app.openapi_schema

app.openapi = custom_openapi


# Enable CORS from anywhere with anything
# TODO: Upgrade to Python 3.8 for current EOL support
# TODO: Add UI to restrict these
# TODO: Fix CORS for new Chrome addition where non-secure localhosts clash
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, list):
        # A list of error messages
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "errors": [{
                    "status": str(exc.status_code),
                    "title": detail
                } for detail in exc.detail]
            }
        )

    # A single string error message
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "errors": [{
                "status": str(exc.status_code),
                "title": exc.detail
            }]
        }
    )


def main() -> None:
    """
    Add our routes to the application
    """
    log_setup()

    logging.info("Starting TRAFFCAP...")

    banner()

    Repository.create_connection()

    logging.info("Checking and migrating...")
    Repository.migrate_up()

    assets_dir = Path(str(Path(__file__).parent), "spa", "dist", "spa", "assets")

    # Static mount for SPA assets, with root files exposed elsewhere
    app.mount(
        "/assets",
        StaticFiles(directory=str(assets_dir)),
        name="spa"
    )

    # API Routes
    for router in api_routers:
        app.include_router(router)

    logging.info("Listening for traffic...")


"""
Direct CLI support
"""
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
    default="0.0.0.0",
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


if __name__ in ["__main__", "server", "traffcap.server"]:
    main()
