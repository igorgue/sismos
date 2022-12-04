#!/bin/env sh

set -e

poetry run uvicorn sismos:app --host 0.0.0.0 --port 6200
