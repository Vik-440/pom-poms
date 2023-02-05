#syntax=docker/dockerfile:experimental
FROM python:3.8-slim-buster
RUN mkdir -p /app_flask
WORKDIR /app_flask
COPY . /app_flask
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
EXPOSE 5000
RUN flask db upgrade
CMD ["flask", "run"]