import docker
import os
import uuid
import asyncio
import random
import re
import time
import multiprocessing
import copy
import time
import json

from .network_check import NetworkCheck

class DockerManager():
    def __init__(self, data_path, supported_containers, container_base_name="collab-vm-", ws_timeout=20, port_range=(11000, 12000)):
        # self.base_url = "ws://10.89.51.134"
        self.base_url   = "ws://127.0.0.1"
        # self.client   = docker.from_env()
        self.client     = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        self.start_port = min(port_range)
        self.end_port   = max(port_range)

        self.__instances_path__     = os.path.join(data_path, "instances")
        self.supported_containers   = supported_containers
        self.container_base_name    = container_base_name
        self.ws_timeout             = ws_timeout
    
    def __get_stream_url__(self, port):
        return f"{self.base_url}:{port}/vnc"

    def __get_ports__(self):
        # TODO: We should also check if port is used by other host services
        used_ports = set()
        for container in self.client.containers.list():
            for ports in container.ports.values():
                if ports:
                    for port in ports:
                        print(port["HostPort"])
                        port = re.findall(r'\d+',port["HostPort"])[0]
                        if self.start_port <= int(port) < self.end_port:
                            used_ports.add(int(port))
        available_ports = set(range(self.start_port, self.end_port+1)) - used_ports
        return random.choice(list(available_ports)) if available_ports else None

    def __get_config_path__(self, uid):
        return os.path.join(self.__instances_path__, uid, "configs.json")

    def __get_volume_path__(self, uid):
        return os.path.join(self.__instances_path__, uid, "data")

    def __get_directory_names__(self, directory):
        directory_names = set()
        for entry in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, entry)):
                directory_names.add(entry)
        return directory_names

    def __generate_uuid__(self):
        uid = str(uuid.uuid4())
        while uid in self.__get_directory_names__(self.__instances_path__):
            uid = str(uuid.uuid4())
        try:
            # Change to makedirs
            os.mkdir(os.path.join(self.__instances_path__, uid))
            os.mkdir(os.path.join(self.__instances_path__, uid, "data"))
            print(f"Directory '{uid}' created successfully.")
            return uid
        except FileExistsError:
            print(f"Directory '{uid}' already exists.")
            return None
        except OSError as e:
            print(f"Error creating directory '{uid}': {str(e)}")
            return None

    def __set_ws_timeout__(self, docker_args):
        if "environment" not in docker_args:
            docker_args["environment"] = {}
        docker_args["environment"]["WS_TIMEOUT"] = self.ws_timeout
        return docker_args

    # Returns a guaranteed to work container
    def parse_container(self, configs):
        if configs.get("vm", "") not in self.supported_containers:
            # TODO: Temporary Fallback, fix later to be safer
            return self.supported_containers["vnc-x11-firefox"]
        
        container_envs = set(self.supported_containers[configs.get("vm")]["environment"].keys())

        final_configs = copy.deepcopy(self.supported_containers[configs.get("vm")])
        for key, param in configs.get("env", {}).items():
            if key in container_envs:
                final_configs["environment"][key] = param
        final_configs["image"] = configs.get("vm")
        
        return final_configs

    def __existing_container_port__(self, uid):
        # TODO: Notable edge case that should be considered: container found but no port detected
        try:
            containers_found = self.client.containers.list(all=True, filters={"name": f"{self.container_base_name}{uid}"})
            if len(containers_found) != 0:
                return [re.findall(r'\d+', port[0]["HostPort"])[0] for port in containers_found[0].ports.values()][0]
        except:
            return None

    def get_existing_container_port(self, uid):
        port = self.__existing_container_port__(uid)
        if (port):
            return self.__get_stream_url__(port), port
        else:
            return None, None

        # return self.__get_stream_url__(port) if port else None

    def load(self, uid=None, docker_args={}):
        # Check if container exists
        port = self.__existing_container_port__(uid)
        if port:
            return self.__get_stream_url__(port), port, uid

        # Allocate
        port = self.__get_ports__()
        if port:
            # Init new if uid doesnt exist in data
            if uid is None or uid not in self.__get_directory_names__(self.__instances_path__):
                uid = self.__generate_uuid__()

            # Start Container
            try:
                # Save configs to make idempotentency when relaunching/ reinstancing
                if os.path.isfile(self.__get_config_path__(uid)):
                    with open(self.__get_config_path__(uid), 'r') as config_file:
                        # TODO: Consider running this through the parser again to guarantee safety incase of file edit
                        docker_args = json.load(config_file)
                else:
                    with open(self.__get_config_path__(uid), 'w') as config_file:
                        json.dump(docker_args, config_file)
                
                # Override/set ws timeout
                docker_args = self.__set_ws_timeout__(docker_args)

                # Create and Launch Container
                container = self.client.containers.run(
                    name=f'collab-vm-{uid}',
                    ports={'2222': port},
                    volumes={
                        self.__get_volume_path__(uid): {'bind': '/root', 'mode': 'rw'}
                    },
                    # cpu_shares=1024,
                    detach=True,
                    remove=True,
                    **docker_args
                )

            except docker.errors.APIError as e:
                print(f"Error starting Firefox container: {str(e)}")
                return "Error starting Firefox container", None

            # # Waiting For Container
            # while container.status != 'running':
            #     print(f"Waiting for container '{uid}' to be ready...")
            #     time.sleep(0.1)
            #     container.reload()

            return self.__get_stream_url__(port), port, uid
        else:
            return "No more resources/ports available", None

    async def await_ws(self, ws_url, port, uid, await_time=1):
        # # Waiting For Container
        # if container != None:
        #     while container.status != 'running':
        #         print(f"Waiting for container '{uid}' to be ready...")
        #         await asyncio.sleep(0.2)
        #         container.reload()

        # Waiting For WS:
        connection_ok = False
        await asyncio.sleep(1)
        for i in range(600):
            print(f"Waiting for connection {ws_url} with {uid} to be ready...")
            connection_ok = await NetworkCheck.check_websocket_connection(ws_url)
            # # DOSS like behaviour slows down boot time, only occured after introduction of nginx
            # await asyncio.sleep(0.1)
            await asyncio.sleep(await_time)

            if connection_ok:
                # decreases probability of error when the prior loop connects too quickly
                await asyncio.sleep(0.1)
                break

        if not connection_ok:
            return "Container status check timed out", None

        print(f"Done '{uid}'")
        return ws_url, port, uid

        