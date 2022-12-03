# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11-alpine
WORKDIR /app

# Install curl
RUN apk add --no-cache curl bash

# Install Poetry
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /app

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY . /app
ENV PYTHONPATH=/app

RUN poetry install --no-dev

ENTRYPOINT [ "/app/run.sh" ]
