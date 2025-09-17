#!/bin/bash
cd "$(dirname "$0")" && cd base-containers

# Base Images
cd baseimage-websockify && ./build.sh && cd ..
cd baseimage-websockify-audio && ./build.sh && cd ..

cd baseimage-websockify-vnc-x11 && ./build.sh  && cd ..
cd baseimage-websockify-vnc-x11-audio && ./build.sh  && cd ..


cd ../containers

# Apps
# for dir in websockify-vnc-x11-*/
for dir in */
do
    (
        cd "$dir"
        ./build.sh
        cd ..
    )
done
