# Dockerfile for my app, a fast api using python 3.11
FROM python:3.11.0a5-alpine3.14
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
