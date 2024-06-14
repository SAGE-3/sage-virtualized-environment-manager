#!/bin/bash
cd "$(dirname "$0")"

./../../build_all_containers.sh && ./../build_docker.sh
