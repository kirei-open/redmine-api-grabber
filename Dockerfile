FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

LABEL maintainer="Alfian Azizi <alfianazizi4869@gmail.com>"

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app

