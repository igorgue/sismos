# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11-slim

ENV IN_DOCKER=1
ENV PYTHONPATH=".:/app"

WORKDIR /app

COPY . .

RUN apt-get update -y
RUN apt-get install curl -y

ENV PATH=/root/.local/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

CMD /app/run.sh
