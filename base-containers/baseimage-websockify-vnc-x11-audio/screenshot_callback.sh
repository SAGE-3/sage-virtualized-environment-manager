#!/bin/bash

export DISPLAY=:99
# Take screenshot as JPEG with high compression
import -window root -format jpeg -quality 80 /tmp/screenshot.jpg 2>/dev/null
if [ -f /tmp/screenshot.jpg ]; then
    screenshot_base64=$(base64 -w 0 /tmp/screenshot.jpg)
    json_data='{"lastImage":"data:image/jpeg;base64,'$screenshot_base64'"}'
    rm /tmp/screenshot.jpg

    if [ -n "$CALLBACK_URL" ]; then
        echo "$json_data" > /tmp/payload.json
        curl -X POST --url $CALLBACK_URL --header "content-type: application/json" --data @/tmp/payload.json
        rm /tmp/payload.json
    fi
fi