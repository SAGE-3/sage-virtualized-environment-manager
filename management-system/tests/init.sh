#!/bin/bash
cd "$(dirname "$0")"

docker run --rm -d --name co-sage-container-manager-test-only \
  -e PYTHONUNBUFFERED=1 \
  -e PORT_RANGE_START=11000 \
  -e PORT_RANGE_END=12000 \
  -e CONTAINER_BASE_NAME=collab-vm- \
  -e CONTAINER_NO_CLIENT_TIMEOUT=$1 \
  -p 4024:4024 \
  -p 4033:4033 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --add-host host.docker.internal:host-gateway \
  --network host \
  co-sage-container-manager:latest


# -v ./data/:/app/data \
