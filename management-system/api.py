from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, StreamingResponse

import httpx
import os
import asyncio

import pycurl
from management import DockerManager


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.system("./init.sh")

app = FastAPI()

# Default callable containers and values
manager = DockerManager(
    data_path=os.path.join(__location__, "data"),
    supported_containers = {
        'websockify-baseimg': {
            "environment": {
                'TARGET_IP': '0.0.0.0',
                'TARGET_PORT': '5900',
            },
        },
        'vnc-x11-firefox': {
            "environment": {
                'FIREFOX_THEME': 0,
                # 'FIREFOX_STARTPAGE': "www.google.com",
            },
        },
        'vnc-x11-doom': {
            "environment": {
            },
        },
        'vnc-x11-blender': {
            "environment": {
            },
        }
    },
    container_base_name=os.environ.get("CONTAINER_BASE_NAME", "collab-vm-"),
    ws_timeout=os.environ.get("CONTAINER_NO_CLIENT_TIMEOUT", 20),
    port_range=(int(os.environ.get("PORT_RANGE_START", 11000)), int(os.environ.get("PORT_RANGE_END", 12000)))
)


def get_sage_url(port):
    # return f"ws://10.89.51.134:4033/vmstream/{port}/vnc"
    return f"/stream/{port}/vnc"

# Multipurpose api call
# Will create new container if uuid does not match, then return websocket and uuid
# Will redeploy container if uuid matches, then return websocket and uuid
# Will return websocket and uuid if container already deployed
@app.post("/api/vm/any/{uid}")
async def handle_assumed_uid_request(uid: str, configs: dict):#, image: {str}):
    global manager
    print("Begin VM Any Request for", uid)

    docker_args = manager.parse_container(configs) # TODO: return error that the container does not exist or whatever
    # docker_args["image"] = "vnc-x11-firefox" # Uncomment to override, only for demo purposes
    ws_url, port, uid = manager.load(uid=uid, docker_args=docker_args)

    print("Blocking Operations Completed for", uid)
    await manager.await_ws(ws_url, port, uid, await_time=1) # TODO: Remove uid from this function later
    return {"url": get_sage_url(port), "uid": uid} if uid else {"details": result}


# Gets returns websocket or empty if no container exists
@app.get("/api/vm/ws/{uid}")
async def handle_ws_get(uid: str):
    global manager
    ws_url, port = manager.get_existing_container_port(uid) # TODO: Convert to async
    # await manager.await_ws(ws_url, port, uid)
    return {"url": get_sage_url(port)} if ws_url else {"details": "container not running"}


# Command to stop/delete containers if running and deletes the stored directories
@app.get("/api/vm/rm/{uid}")
async def handle_delete():
    global manager
    return {"details": "not yet implemented"}

if __name__ == "__main__":
    pass