from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.orders import (
    data_for_main_page,
    changing_status_order,
    changing_phase_produce)

from app.api.order import order

from app.api.client import client

from app.api.product import product

from app.api.materials import extract_materials_data

from app.api.payments import payment

from app.api.outlays import outlay

from app.api.financial import (
    attributes_payments,
    statistics,
    search_payments,
    search_outlay)

from app.api.general import (
    autofill,
    pin_pong)

# from app.api import errors