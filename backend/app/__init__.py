from builtins import Exception
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy import create_engine
from dotenv import load_dotenv
from flask_cors import CORS
import json
import psycopg2
import os
import pytest

from app.config import config
from app.swagger_config import get_swagger_config
from app.base_model import Base
from log.logger import logger

db = SQLAlchemy()
engine = None

@pytest.fixture
def create_app(config_name="development"):
    print(config_name)
    global engine
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app, config=get_swagger_config())
    CORS(app)
    app.config.from_object(config[config_name])

    db.init_app(app)
    
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)
    Base.metadata.create_all(engine)

    # app.engine = engine
    # db.engine = engine

    from app.api import api

    app.register_blueprint(api)
    app.config['WTF_CSRF_ENABLED'] = False

    return app


# load_dotenv()

    # try:
    #     config_name_psql = os.getenv("CONFIG_NAME_PSQL")
    #     print(config_name_psql)
    #     if config_name_psql == 'testing':
    #         db_url = 'sqlite:///:memory:'
    #     elif config_name_psql == 'development':
    #         db_url = os.getenv("PSQL_URL_TEST")
    #     elif config_name_psql == 'product':
    #         db_url = os.getenv("PSQL_URL_PROD")
    #     else:
    #         raise (Exception('Please insert correct setup config_name!'))
    #     engine = create_engine(db_url, future=True)
    #     Base.metadata.create_all(engine)
    # except Exception as e:
    #     logger.error(f'Error in function return_engine: {e}')
