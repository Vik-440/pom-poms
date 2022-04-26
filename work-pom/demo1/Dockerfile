FROM ubuntu:20.04
WORKDIR /code
ENV FLASK_APP=app_flask.py
ENV FLASK_RUN_HOST=127.0.0.2
COPY . .
RUN apt-get update && apt-get install -y python python3-pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]