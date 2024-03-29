from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.orders.models import DB_orders
from app.api.financial.attributes_payments import attributes_payments
from app import engine


def validate_payment(data: dict):
    """Validator payment"""
    if not 'id_order' in data:
        return {'id_order': 'miss in data'}
    if not isinstance(data['id_order'], int):
            return {'id_order': 'is not int type'}
    with Session(engine) as session:
        stmt = (
            select(DB_orders.id_order)
            .where(DB_orders.id_order == data['id_order']))
        if not session.execute(stmt).first():
            return {'id_order': f'ID order {data["id_order"]} is not real'}
        stmt = (
            select(DB_orders.status_order)
            .where(DB_orders.id_order == data['id_order']))
        if session.execute(stmt).scalar():
            return {'id_order': f'ID order {data["id_order"]} is closed'}
    
    if not 'payment' in data:
        return {'payment':  'miss in data'}
    if not isinstance(data['payment'], int):
        return {'payment': 'is not int type'}
    
    if not 'metod_payment' in data:
        return {'metod_payment': 'miss in data'}
    if not isinstance(data['metod_payment'], str):
        return {'metod_payment': 'is not str type'}
    response, status_code = attributes_payments()
    metod_payment = response.get_json()['metod_payment']
    if data['metod_payment'] not in metod_payment:
        return {'metod_payment': 'method is not valid'}
    
    if not 'data_payment' in data:
        return {'data_payment': 'miss in data'}
    if not isinstance(data['data_payment'], str):
        return {'data_payment': 'is not str type'}
    date_str = data['data_payment']
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {'data_payment': 'is not in format like: yyyy-mm-dd'}
    data['data_payment'] = date_str

    return


def validate_search_payment(data: dict):
    if not 'data_start' in data:
        return {'data_start': 'miss in data'}
    if not isinstance(data['data_start'], str):
        return {'data_start': 'is not str type'}
    date_str = data['data_start']
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {'data_start': 'is not in format like: yyyy-mm-dd'}
    data['data_start'] = date_str

    if not 'data_end' in data:
        return {'data_end': 'miss in data'}
    if not isinstance(data['data_end'], str):
        return {'data_end': 'is not str type'}
    date_str = data['data_end']
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {'data_end': 'is not in format like: yyyy-mm-dd'}
    data['data_end'] = date_str

    if not 'iban' in data:
        return {'iban': 'miss in data'}
    if not isinstance(data['iban'], bool):
        return {'iban': 'is not bool type'}
    
    if not 'cash' in data:
        return {'cash': 'miss in data'}
    if not isinstance(data['cash'], bool):
        return {'cash': 'is not bool type'}
    return