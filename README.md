# Sage Virtualized Environment Management
This simple piece of software allows to user to request on demand virtualized environment from a pre-curated list of docker containers.  Virtualized desktop environments are VNC'd to the frontend via websocket and automatically shutdown upon inactivity.

# Bindings
| Container Path        | Function                                                                  |
| -------------         | -------------                                                             |
| /var/run/docker.sock  | Docker socket to establish communications with the host system's docker   | 
| /app/data             | Data where the container's configs and data are stored                    |

> The docker-compose.yml file needs to create a binding with the host systems docker.sock; this implementation will spin up indiviual containers on the host system.  If this is intolerable, consider changing the docker binding another system or inside a docker container.

# Environment Variables
| Variable Name                 | Default Param | Function                                                                  |
| -------------                 | ------------- | -------------                                                             |
| PORT_RANGE_START              | 11000         | Inclusive starting range for ports to be dynamically allocated            | 
| PORT_RANGE_END                | 12000         | Exclusive ending range for ports to be dynamically allocated              |
| CONTAINER_BASE_NAME           | collab-vm-    | Containers will be created with the following schema "collab-vm-{uid}"    |
| CONTAINER_NO_CLIENT_TIMEOUT   | 15            | Time after no active client connections before the container exits        |

> [!CAUTION]  
> Please ensure that the port range is avaliable.  Current implementation does not `ss` or `netsat` port mappings utilized beyond the scope of port allocation by docker.  This will be fixed in a future revision.

> [!NOTE]  
> By default the docker manager will scan for containers starting with `collab-vm-`. To avoid any potential conflicts, ensure that other containers do not adhere to a similiar naming scheme.

# API Endpoints
tbd

curl post ... {} ... "/api/vm/any/{uid}"
- Will create new container if uuid does not match, then return websocket and uuid
- Will redeploy container if uuid matches, then return websocket and uuid
- Will return websocket and uuid if container already deployed
return {"url": get_sage_url(port), "uid": uid} if uid else {"details": result}

curl "/api/vm/ws/{uid}"
- Gets returns {"url": websocket} or {"details": ...} if no container exists

    





Known Bugs:
- There is a potential point of failure where connecting to a container in the exiting phase will cause the prevent the user from connecting until another request is sent.


# Applications
[Blender](https://www.blender.org/)

[FireFox](https://www.mozilla.org/en-US/firefox/)


# General Acknowledgements
[TurboVNC](https://www.turbovnc.org/)

[Websockify](https://github.com/novnc/websockify)

[Nginx](https://nginx.org/en/)

[Docker](https://www.docker.com/)

