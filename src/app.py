"""
Main application that provides user service to trigger tasks
by making POST request on "/" route. This server is hosted on 
APP_PROCESS_PORT (8001).
"""

import json
import uvicorn
import requests
from fastapi import FastAPI
from utils import Message, Item
from config import DAEMON_PROCESS_PORT, APP_PROCESS_PORT

app = FastAPI()

@app.post("/")
async def read_root(msg: Message):
    """
    Main GET function to trigger a request in daemon process
    """
    response = requests.request(
        "GET",
        f"http://localhost:{DAEMON_PROCESS_PORT}",
        data=json.dumps(msg.model_dump()),
        timeout=10
    )
    return response.json()

@app.post("/poll")
async def poll_status(item: Item):
    """
    Webhook function to get polled when daemon process is complete
    """
    print(json.dumps(item.model_dump(), indent=4))

if __name__ == "__main__":
    uvicorn.run("app:app", port=APP_PROCESS_PORT, reload=True)
