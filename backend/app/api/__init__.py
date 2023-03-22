from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.orders import (
    data_for_main_page,
    changing_status_order,
    changing_phase_produce)

from app.api.order import(
    create_order,
    edit_order)

from app.api.client import(
    create_client,
    edit_client)

from app.api.product import(
    create_product,
    edit_product)

from app.api.materials import extract_materials_data

from app.api.payments import (
    last_payments,
    attributes_payments,
    statistics,
    search_payments,
    search_id_payment,
    create_payment,
    edit_payment)

from app.api.outlays import (
    last_outlays,
    edit_outlay,
    create_outlay,
    search_outlay)

from app.api.clients_and_products import (
    all_routs_clients_products)
