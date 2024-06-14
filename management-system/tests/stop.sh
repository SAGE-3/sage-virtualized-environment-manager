#!/bin/bash
cd "$(dirname "$0")"

docker ps -q --filter "name=co-sage-container-manager-test-only" | xargs -r docker kill