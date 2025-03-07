from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, StreamingResponse

import aiohttp

import httpx
import os
import asyncio

import pycurl
from management import DockerManager, docker_pull, docker_network

from foresight.config import config as conf, prod_type
from config import ContainerConfigs


# from dotenv import load_dotenv
# load_dotenv() # load from .env file

prod_type = os.getenv("ENVIRONMENT", "development")
sage3_app_url = f'{conf[prod_type]["web_server"]}/api/apps'
print(conf)
sage3_app_url = sage3_app_url.replace(":3000:3333/api/apps", ":3000/api/apps") # Temporary fix to combat the revert of port 3333 -> 3000
jwt_token = os.getenv('TOKEN', '')
print(sage3_app_url)
print()
print("Running in", prod_type, "mode")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.system("./init.sh")

app = FastAPI()

if prod_type.lower() != "development":
    for key, image in ContainerConfigs.prod_container_mapping.items():
        docker_pull(image)

container_mapping = ContainerConfigs.prod_map_func if prod_type.lower() != "development" else ContainerConfigs.dev_map_func

# Default callable containers and values
manager = DockerManager(
    data_path               = os.path.join(__location__, "data"),
    container_mapping       = container_mapping,
    supported_containers    = ContainerConfigs.supported_containers,
    container_base_name     = os.environ.get("CONTAINER_BASE_NAME", "collab-vm-"),
    ws_timeout              = os.environ.get("CONTAINER_NO_CLIENT_TIMEOUT", 20),
    port_range              = (int(os.environ.get("PORT_RANGE_START", 11000)), int(os.environ.get("PORT_RANGE_END", 12000))),
    network                 = docker_network()
)
print("Init Done")

def get_sage_url(port):
    # return f"ws://10.89.51.134:4033/vmstream/{port}/vnc"
    # if prod_type.lower() != "development":
    # else:
    #     return f"/stream/{port}"
    return f"/api/vmstream/{port}"

# Multipurpose api call
# Will deploy new container if uuid does not match, then return websocket and uuid
# Will return websocket and uuid if container already deployed
@app.post("/api/vm/any/{uid}")
async def handle_assumed_uid_request(uid: str, configs: dict):#, image: {str}):
    global manager
    print(f"[{uid}]: Begin VM Any Request for")

    docker_args = manager.parse_container(configs) # TODO: return error that the container does not exist or whatever
    # docker_args["image"] = "vnc-x11-firefox" # Uncomment to override, only for demo purposes
    ws_url, port, uid = manager.load(uid=uid, docker_args=docker_args)

    print(f"[{uid}]: Blocking Operations Completed")
    await manager.await_ws(ws_url, port, uid, await_time=1) # TODO: Remove uid from this function later
    return {"url": get_sage_url(port), "uid": uid} if uid else {"details": result}


# Gets returns websocket or empty if no container exists
@app.get("/api/vm/ws/{uid}")
async def handle_ws_get(uid: str):
    global manager
    ws_url, port = manager.get_existing_container_port(uid) # TODO: Convert to async
    # await manager.await_ws(ws_url, port, uid)
    return {"url": get_sage_url(port)} if ws_url else {"details": "container not running"}


@app.get("/api/vm/list")
async def get_all_uids():
    global manager
    containers = manager.find_containers()
    return [container.name.replace(f"{manager.container_base_name}", "") for container in containers]


@app.post("/api/vm/cb/{uid}")
async def handle_callback(uid: str, configs: dict):
    global jwt_token
    global sage3_app_url
    print(f"[{uid}]: Callback request")
    try:
        data = {"state.urls": configs["urls"]}
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.put(f'{sage3_app_url}/{uid}', 
                                    headers=headers, 
                                    json=data)
            return {"ok"}
    except Exception as e:
        print("callback error", e)

    return {"failed"}


# # Direct push to redis callback method
# #
# # from redis import Redis
# from rejson import Client, Path
# @app.post("/api/vm/cb/{uid}")
# async def handle_callback(uid: str, configs: dict):
#     # global manager
#     # print(configs)

#     try:
#         # redis_client = Redis(host='host.docker.internal', port=6379, decode_responses=True)
#         # JSON.SET "SAGE3:DB:APPS:59bd2c7d-4461-4ab5-9938-0b9183cdee93" .data.state.urls '["www.google.com"]'

#         json_client = Client(host='localhost', port=6379, decode_responses=True)
#         json_client.jsonset(f"SAGE3:DB:APPS:{uid}", Path('.data.state.urls'), configs["urls"])
#     except Exception as e:
#         print(e)
#     return {}

if __name__ == "__main__":
    pass