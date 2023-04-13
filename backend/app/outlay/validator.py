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

