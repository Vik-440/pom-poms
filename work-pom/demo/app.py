from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


with app.app_context():
    from routes.main import *


if __name__ == '__main__':
    app.run(debug=False)
