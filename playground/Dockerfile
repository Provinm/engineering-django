FROM python:3.9-bullseye

COPY . /var/www/src
WORKDIR /var/www/src

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN apt update && apt install make
