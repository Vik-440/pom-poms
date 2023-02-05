from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
import os


db = SQLAlchemy()
migration = Migrate()


def create_app(environment="development"):
    from config import config
    from app.models.directories import directory_of_client, directory_of_color, directory_of_order, directory_of_outlay, directory_of_model, directory_of_payment
    from app.views.main import main_blueprint


    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)
    db.init_app(app)
    migration.init_app(app, db)
    
    app.register_blueprint(main_blueprint)



    return app