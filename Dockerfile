FROM python:3.12-slim

WORKDIR /app

ADD . /app
COPY pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry==1.5.1

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-cache


EXPOSE $PORT
CMD uvicorn app:app --host 0.0.0.0 --port $PORT