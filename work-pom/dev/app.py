from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
port = int(os.getenv("PORT"))


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


with app.app_context():
    from routes.main import *  # noqa: F401, F403


if __name__ == '__main__':
    app.run(debug=True, port=port)
