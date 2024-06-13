#!/bin/bash
echo "Starting Nginx..."
nginx

echo "Starting Websockify..."
websockify 0.0.0.0:3499 $TARGET_IP:$TARGET_PORT --idle-timeout=$WS_TIMEOUT
