#!/bin/bash

set -m

cd "$(dirname "$0")"

# use --reload and celery log level debug if $DEV is set
if [ -n "$DEV" ]; then
    RELOAD="--reload"
fi

# initial scripts
poetry run python sismos/fetch_initial_data.py

# Add cronjob to fetch data every 5 minutes
if [ -n "$IN_DOCKER" ]; then
    echo '*/5 * * * * poetry run python sismos/fetch_initial_data.py' | crontab -
fi

# services
poetry run uvicorn sismos:app --host 0.0.0.0 --port 6200 $RELOAD &

fg %1
