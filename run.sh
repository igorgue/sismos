#!/bin/env sh

set -m

# use --reload if $RELOAD is set
if [ -n "$RELOAD" ]; then
    RELOAD="--reload"
fi

poetry run uvicorn sismos:app --host 0.0.0.0 --port 6200 $RELOAD &
poetry run celery -A sismos.tasks worker -l info &

fg %1
