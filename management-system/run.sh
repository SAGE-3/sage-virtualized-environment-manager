#!/bin/bash

# # Extract the IP for host.docker.internal from /etc/hosts
# HOST_IP=$(grep host.docker.internal /etc/hosts | awk '{print $1}')

# # Replace placeholder in nginx config
# sed -i "s/host.docker.internal/$HOST_IP/g" /etc/nginx/nginx.conf

sed -i "s/host.docker.internal/$(getent hosts host.docker.internal | awk '{ print $1 }')/g" /etc/nginx/nginx.conf

nginx
uvicorn api:app --reload --host 0.0.0.0 --port 4024