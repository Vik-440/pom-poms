from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.orders import main_page
