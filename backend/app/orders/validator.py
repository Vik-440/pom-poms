from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.clients.models import DB_client
from app.products.models import DB_product
from app.orders.models import DB_orders
from utils.validators import validate_field
from app import engine


def validate_id_order(id_order: int):
    """Validator for ID order number"""
    with Session(engine) as session:
        stmt = (
            select(DB_orders.id_order)
            .where(DB_orders.id_order == id_order))
        if not session.execute(stmt).first():
            return {'id_order': f'ID order {id_order} is not exist'}
    return


def validate_phase(phase_data, qty_products_order, phase_name):
    """ Validate phase data based on the quantity of products in the order"""

    if len(phase_data) != qty_products_order:
        return {phase_name: 'misstake in qty phases in data'}
    
    for phase in phase_data:
        if not isinstance(phase, int):
            return {phase_name: 'has data not int type'}
    return


def validate_phases(id_order: int, data: dict):
    """Validate phases for the given order ID and data"""

    with Session(engine) as session:
        stmt = (
            select(DB_orders.id_models)
            .where(DB_orders.id_order == id_order))
        gty_products_in_order = session.execute(stmt).scalar()
        qty_products_order = len(gty_products_in_order)

        for phase_name in ['phase_1', 'phase_2', 'phase_3']:
            if phase_name in data:
                error = validate_phase(data[phase_name], qty_products_order, phase_name)
                if error:
                    return error
    return


def validate_status(data: dict):
    """validate data for chenging status"""
    if not 'status_order' in data:
        return {'status_order': 'miss in data'}
    if not isinstance(data['status_order'], bool):
            return {'status_order': 'is not bool type'}
    return


def validate_date_format(date_str: str, field_name: str):
    """Validator for date format: yyyy-mm-dd"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {field_name: 'is not in format like: yyyy-mm-dd'}
    return


def validate_phase_into(data: dict, phase_name: str, qty_product_in_order: int, factor: int):
    """Validator phases"""
    if qty_product_in_order != len(data[phase_name]):
        return {phase_name: f'qty positions in {phase_name} is not equal qty in id_models'}

    for index, phase_item in enumerate(data[phase_name]):
        if not isinstance(phase_item, int):
            return {phase_name: f'{phase_item} in {phase_name} is not int type'}
        if data['qty_pars'][index] * factor < phase_item:
            return {phase_name: f'{phase_item} in {phase_name} is bigger than it is possible (qty_pars * {factor})'}
    return None


def validate_create_order(data: dict):
    """Validator for create order"""
    qty_product_in_order = None
    date_today = datetime.today().strftime('%Y-%m-%d')
    fields_to_check = [
        ('date_create', str),
        ('date_plane_send', str),
        ('id_client', int),
        ('id_recipient', int),
        ('status_order', bool),
        ('sum_payment', int),
        ('discount', int),
        ('comment', (str, type(None))),
        ('id_models', list),
        ('qty_pars', list),
        ('phase_1', list),
        ('phase_2', list),
        ('phase_3', list),
        ('price_model_sell', list)]
    for field, field_type in fields_to_check:
        error = validate_field(field, field_type, data)
        if error:
            return error
        
    with Session(engine) as session:

        for date_field in ['date_create', 'date_plane_send']:
            error = validate_date_format(data[date_field], date_field)
            if error:
                return error
            if date_field == 'date_create' and data[date_field] > date_today:
                return {date_field: 'date future -> misstake'}

        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == data['id_client']))
        if not session.execute(stmt).first():
            return {'id_client': 'ID is not real'}

        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == data['id_recipient']))
        if not session.execute(stmt).first():
            return {'id_recipient': 'ID is not real'}

        qty_product_in_order = len(data['id_models'])
        if qty_product_in_order == 0:
            return {'id_models': 'is empty'}
        for id_product in data['id_models']:
            if not isinstance(id_product, int):
                return {'id_models': f'{id_product} is not int type'}
            stmt = (
                select(DB_product.id_product)
                .where(DB_product.id_product == id_product))
            if not session.execute(stmt).first():
                return {'id_models': f'ID product {id_product} is not real'}

        if qty_product_in_order != len(data['qty_pars']):
            return {'qty_pars': 'qty positions in qty_pars is not eiqual qty in id_models'}
        for qty_pars_item in data['qty_pars']:
            if not isinstance(qty_pars_item, int):
                return {'qty_pars': f'{qty_pars_item} in qty_pars is not int type'}

        error = validate_phase_into(data, 'phase_1', qty_product_in_order, 2)
        if error:
            return error

        error = validate_phase_into(data, 'phase_2', qty_product_in_order, 2)
        if error:
            return error

        error = validate_phase_into(data, 'phase_3', qty_product_in_order, 1)
        if error:
            return error

        if qty_product_in_order != len(data['price_model_sell']):
            return {'price_model_sell': 'qty positions in price_model_sell is not eiqual qty in id_models'}
        for price_model_sell_item in data['price_model_sell']:
            if not isinstance(price_model_sell_item, int):
                return {'price_model_sell': f'{price_model_sell_item} in price_model_sell is not int type'}

    return 
