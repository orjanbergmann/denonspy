FROM python:3.12-slim-bookworm
MAINTAINER Ørjan Bergmann

## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd && \
    apt-get install -y gcc && \
    apt-get install -y build-essential && \
    apt-get install -y i2c-tools && \
    apt-get install -y libpq-dev && \
    apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . .

CMD ["python3", "main.py"]
