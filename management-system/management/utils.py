import socket
import subprocess
import json

import docker

def docker_pull(image_name):
    try:
        # Initialize Docker client
        client = docker.from_env()
        
        # Pull the image
        # You can print the pull progress by looping through the output
        print(f"Pulling image: {image_name}")
        for line in client.api.pull(image_name, stream=True, decode=True):
            if 'progress' in line:
                print(f"{line.get('id', '')}: {line.get('progress', '')}")
            elif 'status' in line:
                print(f"{line.get('id', '')}: {line.get('status', '')}")
        
        print(f"Successfully pulled image: {image_name}")
        return True
    except docker.errors.APIError as e:
        print(f"Error pulling image: {e}")
        return False

# This is a hacky way to get the first network, not terrible robust when the external configuration changes
def docker_network():
    try:
        container_id = socket.gethostname()
        # print(container_id)

        command = f"curl --unix-socket /var/run/docker.sock http://localhost/containers/{container_id}/json"
        result = subprocess.check_output(command, shell=True)
        container_info = json.loads(result)

        # Extract network info
        networks = container_info.get('NetworkSettings', {}).get('Networks', {})
        network = ""
        for network_name, network_details in networks.items():
            network = network_name
            print(f"Connected to network: {network_name} using {container_id}")
            break
        return network
    except:
        return ""
