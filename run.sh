#!/bin/env sh

set -e

cd sismos
uvicorn sismos:app --host 0.0.0.0 --port 6200
