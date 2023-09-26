from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from sqlalchemy import create_engine

from app.config import config
from app.swagger_config import get_swagger_config
from app.base_model import Base

engine = None


# def create_app(config_name="development"):
def create_app(config_name="production"):
    print(config_name)
    global engine
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app, config=get_swagger_config()) # noqa
    CORS(app)
    app.config.from_object(config[config_name])

    with app.app_context():
        engine = create_engine(
            app.config['SQLALCHEMY_DATABASE_URI'],
            future=True
        )
        Base.metadata.create_all(engine)

    from app.api import api

    app.register_blueprint(api)
    app.config['WTF_CSRF_ENABLED'] = False

    return app
