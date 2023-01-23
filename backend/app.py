# from app import create_app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(load_dotenv=True, host='127.0.0.2')


from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"
    