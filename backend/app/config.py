from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("PSQL_URL_PROD")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("PSQL_URL_TEST")

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = os.getenv("PSQL_URL_PYTEST")

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}