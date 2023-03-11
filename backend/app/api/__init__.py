from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.orders import data_for_main_page
from app.api.orders import changing_status_order
from app.api.orders import changing_phase_produce

from app.api.materials import extract_materials_data
# from app.api.orders 
