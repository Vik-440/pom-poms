from datetime import datetime

from app.api.financial.attributes_payments import attributes_payments


def validate_outlay(data: dict):
    """Validator outlay"""
    if not 'data_outlay' in data:
        return {"data_outlay": 'miss in data'}
    if not isinstance(data['data_outlay'], str):
        return {'data_outlay': 'is not str type'}
    date_str = data['data_outlay']
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {'data_outlay': 'is not in format like: yyyy-mm-dd'}
    data['data_outlay'] = date_str

    if not 'id_outlay_class' in data:
        return {'id_outlay_class': 'miss in data'}
    if not isinstance(data['id_outlay_class'], str):
        return {'id_outlay_class': 'is not str type'}
    response, status_code = attributes_payments()
    metod_payment = response.get_json()['outlay_class']
    if data['id_outlay_class'] not in metod_payment:
        return {'id_outlay_class': 'is not valid'}

    if not 'money_outlay' in data:
        return {"money_outlay":  "miss in data"}
    if not isinstance(data['money_outlay'], int):
        return {'money_outlay': 'is not int type'}

    if not 'comment_outlay' in data:
        return {'comment_outlay': 'miss in data'}
    if not isinstance(data['comment_outlay'], str):
        return {'comment_outlay': 'is not str type'}
    return

def validate_search_outlay(data: dict):
    """Validator search outlay"""
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


def validate_balance(data: dict):
    """validate request for balance"""
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

    # if not 'balans' in data:
    #     return {'balans': 'miss in data'}
    if not isinstance(data['balans'], str):
        return {'balans': 'is not str type'}
    time_period_str = ['day', 'week', 'month', 'quarter', 'year']
    if data['balans'] not in time_period_str:
        return {'balans': 'key is not valid'}
    
    if not 'iban' in data:
        return {'iban': 'miss in data'}
    if not isinstance(data['iban'], bool):
        return {'iban': 'is not bool type'}
    
    if not 'cash' in data:
        return {'cash': 'miss in data'}
    if not isinstance(data['cash'], bool):
        return {'cash': 'is not bool type'}
