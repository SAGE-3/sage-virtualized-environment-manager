#!/bin/bash

nginx
uvicorn api:app --reload --host 0.0.0.0 --port 4024