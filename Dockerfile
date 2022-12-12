# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11.1-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache curl bash

ENV PATH=/root/.local/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app

CMD /app/run.sh
