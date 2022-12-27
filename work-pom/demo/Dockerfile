#syntax=docker/dockerfile:experimental
FROM python:3.8-slim-buster
RUN mkdir -p /app_flask
WORKDIR /app_flask
COPY . /app_flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# RUN pip3 install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
