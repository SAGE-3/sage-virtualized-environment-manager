#!/bin/bash
cd "$(dirname "$0")" && cd containers

# Base Images
cd baseimage-websockify && ./build.sh && cd ..
cd baseimage-websockify-vnc-x11 && ./build.sh  && cd ..

# Apps
for dir in websockify-vnc-x11-*/
do
    (
        cd "$dir"
        ./build.sh
        cd ..
    )
done