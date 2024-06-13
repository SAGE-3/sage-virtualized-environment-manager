#!/bin/bash
cd "$(dirname "$0")"

./build_all_containers.sh
cd management-system && ./build_run_docker.sh