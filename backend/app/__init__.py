from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# from flask_swagger import swagger
from flasgger import Swagger
from sqlalchemy import create_engine
from dotenv import load_dotenv
from flask_cors import CORS
import psycopg2
import os

from app.config import config
from app.base_model import Base
from log.logger import logger


def create_app(config_name='development'):
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app)
    CORS(app)
    # app.config.from_object('config.Config')
    # app.config.from_object(config[config_name])

    app.config['WTF_CSRF_ENABLED'] = False
    
    from app.api import api

    app.register_blueprint(api)

    return app


load_dotenv()
# config_name = 'development'
config_name = 'product'

try:
    if config_name == 'testing':
        db_uri = psycopg2.connect(':memory:')
    elif config_name == 'development':
        db_uri = os.getenv("PSQL_URL_TEST")
    elif config_name == 'product':
        db_uri = os.getenv("PSQL_URL")
    else:
        raise (Exception('Please insert correct setup config_name!'))
except Exception as e:
    logger.error(f'Error in function return_engine: {e}')

engine = create_engine(db_uri, future=True)
Base.metadata.create_all(engine)
