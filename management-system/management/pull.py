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