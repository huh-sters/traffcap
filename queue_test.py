#!/usr/bin/env python3
from multiprocessing import Manager
from fastapi import FastAPI
"""
Working experiment with multi-process managers

Add a count to a shared dictionary and each websocket server
connection looks for a change and then sends the latest messages to any
connected frontends.

Depends on gunicorn's --preload parameter which runs the following code
in the main server process before the workers are started.
"""

# This is run in the main applications process
manager = Manager()
store = manager.dict()
store["count"] = 0

# Standard FastAPI stuff from here on down
app = FastAPI()


@app.post("/increment")
async def increment():
    store["count"] += 1


@app.get("/count")
async def get_count():
    return store["count"]
