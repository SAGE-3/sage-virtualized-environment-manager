#!/bin/bash
echo "Starting Nginx..."
# nginx -t
# nginx --with-stream=dynamic
nginx

echo "Starting Websockify..."
# AUDIO
# websockify 0.0.0.0:7772 localhost:7773
# VNC
websockify 0.0.0.0:3499 $TARGET_IP:$TARGET_PORT --idle-timeout=$WS_TIMEOUT
