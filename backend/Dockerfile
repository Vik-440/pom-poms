#syntax=docker/dockerfile:experimental
FROM python:3.8-slim-buster
LABEL maintainer="pom-poms database"

RUN mkdir -p /app_flask
WORKDIR /app_flask
COPY . /app_flask


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]