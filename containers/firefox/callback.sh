#!/bin/bash

prior='{"state.urls":[]}'

while true; do
    mapfile -t my_array < <(/./dejsonlz4 $HOME/.mozilla/firefox/*default-esr/sessionstore-backups/recovery.jsonlz4 | jq -r '.windows[].tabs[].entries[-1].url')
    json_array=$(printf '%s\n' "${my_array[@]}" | jq -R . | jq -cs .)
    json_array='{"state.urls":'$json_array'}'
    if [ $prior != $json_array ]; then
        echo "$json_array"
        prior=$json_array
        # if [ -n "$CALLBACK_URL" ] && [ -n "$CALLBACK_TOKEN" ]; then
        if [ -n "$CALLBACK_URL" ]; then

            # echo "Authorization: Bearer $CALLBACK_TOKEN"
            # Consider Parsing the callbacks (i.e., spacing)
            # curl --request PUT --url $CALLBACK_URL --header "Authorization: Bearer $CALLBACK_TOKEN" --header "content-type: application/json" --data "$json_array"

            curl -X POST --url $CALLBACK_URL --header "content-type: application/json" --data "$json_array"
        fi
    fi

    sleep 1
done;