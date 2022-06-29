from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "Welcome!"


@app.route('/hello')
def hello():
    return "Hi there!"


@app.route('/my_name')
def my_name():
    return "Hi, I'm Yurii Kavetskyi!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
