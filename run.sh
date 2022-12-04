#!/bin/env sh

set -m

# use --reload and celery log level debug if $DEV is set
if [ -n "$DEV" ]; then
    RELOAD="--reload"
    CELERY_LOG_LEVEL="debug"
else
    CELERY_LOG_LEVEL="info"
fi

poetry run uvicorn sismos:app --host 0.0.0.0 --port 6200 $RELOAD &
poetry run celery -A sismos.tasks worker -B -l $CELERY_LOG_LEVEL &

fg %1
