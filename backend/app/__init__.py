# from builtins import Exception
from flask import Flask #, jsonify, request
from flask_restful import Api #, Resource
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy import create_engine
# from dotenv import load_dotenv
from flask_cors import CORS

from app.config import config
from app.swagger_config import get_swagger_config
from app.base_model import Base
from log.logger import logger

engine = None

def create_app(config_name="development"):
    print(config_name)
    global engine
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app, config=get_swagger_config())
    CORS(app)
    app.config.from_object(config[config_name])
    db = SQLAlchemy(app)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)
    Base.metadata.create_all(engine)

    from app.api import api

    app.register_blueprint(api)
    app.config['WTF_CSRF_ENABLED'] = False

    return app


