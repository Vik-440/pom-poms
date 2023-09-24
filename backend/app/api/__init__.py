from flask import Blueprint

api = Blueprint('api', __name__)

from app.api.orders import ( # noqa(F401)
    data_for_main_page,
    changing_status_order,
    changing_phase_produce)

from app.api.order import order # noqa(F401)

from app.api.client import client # noqa(F401)

from app.api.product import product # noqa(F401)

from app.api.materials import material # noqa(F401)

from app.api.payments import payment # noqa(F401)

from app.api.outlays import outlay # noqa(F401)

from app.api.financial import ( # noqa(F401)
    attributes_payments,
    statistics,
    search_payments,
    search_outlay)

from app.api.general import ( # noqa(F401)
    autofill,
    pin_pong)

from app.api.param_db import param_view # noqa(F401)
