FROM python:3.11-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONPATH=/app/src

COPY src /app/

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -q -r /app/requirements.txt
RUN apt-get update && apt-get install -y libgomp1

EXPOSE 8000

CMD uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
