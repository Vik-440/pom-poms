from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2
import os

from app.config import config
from app.base_model import Base

load_dotenv()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    try:
        if config_name == 'testing':
            db = psycopg2.connect(':memory:')
        elif config_name == 'development':
            db = os.getenv("PSQL_URL_TEST")
        else:
            raise (Exception('Please insert correct setup config_name!'))
    except Exception as e:
        pass
        # logger.error(f'Error in function return_engine: {e}')

    engine = create_engine(db, future=True)
    Base.metadata.create_all(engine)

    from app.api import api

    app.register_blueprint(api)

    return app
