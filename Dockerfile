# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11-alpine

COPY . /app

WORKDIR /app


# Install curl
RUN apk add --no-cache curl bash

# Add .local/bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app
ENTRYPOINT ["sh", "run.sh"]
