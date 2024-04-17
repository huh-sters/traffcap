from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from traffcap.core import Metric
"""
Prometheus exporter endpoint
============================

TODO: Make the Prometheus exporter work
"""


metrics_router = APIRouter(prefix="/metrics", tags=["Metrics"])


@metrics_router.get("")
async def metrics_get() -> PlainTextResponse:
    """
    Gather all metrics for exporting to prometheus
    1. Keep a list of sources of metrics
    2. Build a list of metric responses
    3. Export them out as a plain text response

    Metrics:
    * traffcap_requests (endpoint_code, method, count)
    * traffcap_actions (number of matching actions)
    * traffcap_users (number of users)
    * traffcap_groups (number of groups)
    """
    metrics = [
        Metric(
            type="traffcap_total_requests",
            help="Total number of requests received",
            data={
                "url": "http://localhost"
            },
            value=100
        )
    ]
    return PlainTextResponse("".join([str(metric) for metric in metrics]))
