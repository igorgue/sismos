# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11-alpine

COPY . /app

WORKDIR /app

RUN apk add --no-cache curl bash

ENV PATH=/root/.local/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app
ENTRYPOINT ["sh", "run.sh"]
