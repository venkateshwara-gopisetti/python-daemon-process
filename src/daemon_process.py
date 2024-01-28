"""
Background application that creates threads and spawns tasks asynchronously based on triggers from application.
by making POST request on "/" route. This server is hosted on 
DAEMON_PROCESS_PORT (8000).
"""

from uuid import uuid4, UUID
from threading import Thread, get_ident
from datetime import datetime
from random import randint 
from uvicorn import run as uvicorn_run
import json
from time import sleep as time_sleep
from config import APP_PROCESS_PORT, DAEMON_PROCESS_PORT
import requests

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """
    """
    tr = TestThreading()
    return {
        "request_id":tr.id,
        "thread_ident":str(get_ident()),
        "timestamp":str(datetime.now()),
        "status": "recieved",
    }

def uuid_convert(obj):
    """
    """
    if isinstance(obj, UUID):
        return obj.hex

class TestThreading():
    """
    """
    def __init__(self):
        self.id = None
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """
        """
        self.id = uuid4()
        print(str(datetime.now()) + ' : Recieved Task : ' + self.id.hex +  " on Thread : " + str(get_ident()))
        time_sleep(randint(5,20))
        print(str(datetime.now()) + ' : Completed Task : ' + self.id.hex +  " on Thread : " + str(get_ident()))
        response = requests.request(
            "POST",
            f"http://localhost:{APP_PROCESS_PORT}/poll",
            timeout=15,
            data=json.dumps({
                "request_id":str(self.id),
                "thread_ident":str(get_ident()),
                "timestamp":str(datetime.now()),
                "status": "completed"
            },
            default=uuid_convert)
        )
        return response.status_code

if __name__ == "__main__":
    uvicorn_run("daemon_process:app", port=DAEMON_PROCESS_PORT, reload=True)
