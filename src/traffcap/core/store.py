from typing import AsyncGenerator, Any
from multiprocessing import Manager

# The default message broker
manager = Manager()
store = manager.dict()

def start_store() -> None:
    """
    Start the store
    """
    global store
    store["last_message"] = 0

def new_traffic_notification() -> None:
    """
    Trigger a message to any listening web sockets
    """
    global store
    store["last_message"] += 1

async def wait_for_notification() -> AsyncGenerator[Any, Any]:
    """
    Wait for a change in the last_message. By default this uses
    the stdlib multiprocessing Manager. Which is good for ASGI/WSGI
    worker threads with something like gunicorn and uvicorn. However,
    if this application is to be scaled up, then a third party message
    broker will be necessary. The preferred solution is RabbitMQ, but
    this should also support Redis.
    """
    try:
        last_message = store.get("last_message", 0)
        while last_message == store.get("last_message", 0):
            yield
    except EOFError:
        pass
