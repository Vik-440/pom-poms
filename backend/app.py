from app import create_app
from dotenv import load_dotenv
import os


load_dotenv()
config_name = os.getenv("CONFIG_NAME_PSQL")


if __name__ == '__main__':
    app = create_app(config_name)
    app.run(load_dotenv=True, host='127.0.0.1', debug=True)
