from builtins import Exception
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
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
    
    from app.api import api

    app.register_blueprint(api)
    app.config['WTF_CSRF_ENABLED'] = False

    return app


load_dotenv()

try:
    config_name_psql = os.getenv("CONFIG_NAME_PSQL")
    print(config_name_psql)
    if config_name_psql == 'testing':
        db_url = 'sqlite:///:memory:'
    elif config_name_psql == 'development':
        db_url = os.getenv("PSQL_URL_TEST")
    elif config_name_psql == 'product':
        db_url = os.getenv("PSQL_URL_PROD")
    else:
        raise (Exception('Please insert correct setup config_name!'))
    engine = create_engine(db_url, future=True)
    Base.metadata.create_all(engine)
except Exception as e:
    logger.error(f'Error in function return_engine: {e}')


