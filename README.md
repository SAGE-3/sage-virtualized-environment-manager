# Sage Virtualized Environment Manager (CoSage)

This simple piece of software allows to user to request on demand virtualized environment from a pre-curated list of docker containers. Virtualized desktop environments vnc connection is tunneled via websockify and proxied by Nginx to the frontend with automatic shutdown upon inactivity.

## Host Dependencies

- [Docker](https://www.docker.com/)

## Bindings

| Container Path       | Function                                                                |
| -------------------- | ----------------------------------------------------------------------- |
| /var/run/docker.sock | Docker socket to establish communications with the host system's docker |

> The docker-compose.yml file needs to create a binding with the host systems docker.sock; this implementation will spin up sibling containers on the host system. If this is intolerable, consider changing the docker binding another system or inside a docker container.

## Environment Variables

| Variable Name               | Default Param | Function                                                               |
| --------------------------- | ------------- | ---------------------------------------------------------------------- |
| PORT_RANGE_START            | 11000         | Inclusive starting range for ports to be dynamically allocated         |
| PORT_RANGE_END              | 12000         | Exclusive ending range for ports to be dynamically allocated           |
| CONTAINER_BASE_NAME         | collab-vm-    | Containers will be created with the following schema "collab-vm-{uid}" |
| CONTAINER_NO_CLIENT_TIMEOUT | 15            | Time after no active client connections before the container exits     |

> [!CAUTION]  
> Please ensure that the port range is avaliable. Current implementation does not `ss` or `netsat` port mappings utilized beyond the scope of port allocation by docker. This will be fixed in a future revision.

> [!WARNING]  
> By default the docker manager will scan for containers starting with `collab-vm-`. To avoid any potential conflicts, ensure that other containers do not adhere to a similiar naming scheme.

## API Endpoints

[http://localhost:4024/docs](http://localhost:4024/docs): TBD

### API Management

Management API, by default, exists on port 4024

#### Requesting Containter

- Will deploy new container if uid does not match, then return websocket and uuid
- Will return websocket and uuid if container already deployed

<br>
<br>

##### Unknown UID request example:

> [!NOTE]
> You may choose to declare any alternative to `allocate` as long as it does not match with a pre-existing data directory

```bash
curl http://localhost:4024/api/vm/any/allocate -H "Content-Type: application/json" -d '{"vm": "vnc-x11-firefox", "env": {}}'
```

upon success will return

```json
{ "url": "/stream/11446/vnc", "uid": "0984ae47-6fb9-48bd-8f48-8afd7e462762" }
```

In this peticular example, the url returned is specifically designed to be proxied by the Sage3 frontend. You may adjust the return url if you wish to migrate this out of Sage3

<br>
<br>

##### Known UID request example:

As an example, the following UID shall be filled in with `0984ae47-6fb9-48bd-8f48-8afd7e462762`.

> [!NOTE]
> If the given uid matches the uid stored in data, the POST request may be blank as in `{}`, any new given parameters such as `{"vm": "vnc-x11-firefox", "env": {}}` will be ignored. Instead, containers spun up will use the variables provided during setup.

```bash
curl http://localhost:4024/api/vm/any/<uid> -H "Content-Type: application/json" -d '{"vm": "vnc-x11-firefox", "env": {}}'
```

upon success will return

```json
{ "url": "/stream/11535/vnc", "uid": "0984ae47-6fb9-48bd-8f48-8afd7e462762" }
```

<br>
<br>

#### Checking Container Activity State

- Main differentiator is the absence of container startup capabilities, treat this as a ping to the container

#### Example:

```bash
curl "/api/vm/ws/<uid>"
```

returns

```json
{ "url": "/stream/<port>/vnc" }
```

### Container Stream

Containers proxied with Nginx, by default, exist on port 4033

<br>
<br>

### Known Bugs

- There is a potential point of failure where connecting to a container in the exiting phase will cause the prevent the user from connecting until another request is sent.

# Applications

[Blender](https://www.blender.org/)

[FireFox](https://www.mozilla.org/en-US/firefox/)

# General Acknowledgements

[TurboVNC](https://www.turbovnc.org/)

[Websockify](https://github.com/novnc/websockify)

[Nginx](https://nginx.org/en/)

[Docker](https://www.docker.com/)
