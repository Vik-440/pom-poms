FROM python:3.8-slim-buster
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]

# sudo docker build -t first_d_app .
# sudo docker run -p 5000:5000 first_d_app