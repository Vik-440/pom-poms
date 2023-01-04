from flask import request
from app import app

from functions.finance.finance_crate_data import (
    creating_payment,
    creating_outlay)
from functions.finance.finance_change_data import (
    payment_changing,
    outlay_changing)
from functions.finance.finance_statistics import (
    return_data_from_payment_stat,
    return_data_from_payment_balans)
from functions.finance.finance_search_filter import (
    payment_searching,
    outlay_searching,
    payment_id_order_searching)
from functions.finance.finance_start_requests import (
    opening_last_payments,
    opening_last_outlays)
from log.logger import logger


@app.route('/finance', methods=['POST'])
def finance():
    try:
        request.data = request.get_json()
        if 'outlay_search' in request.data:
            return (outlay_searching(request.data)), 200
        elif 'stat' in request.data:
            return (return_data_from_payment_stat(request.data)), 200
        else:
            return ({"message": "finance POST error"}), 500
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/payments/statics', methods=['POST'])
def fin_pay_balans():
    try:
        request.data = request.get_json()
        if 'balans' in request.data:
            return (return_data_from_payment_balans(request.data)), 200
        else:
            return ({"message": "payments/statics is error"}), 500
    except Exception as e:
        logger.error(f'Error in finance payments balans POST: {e}')
        return f'Error in finance payments statics balans: {e}', 500


@app.route('/finance/payments', methods=['POST'])
def fin_pay_search():
    try:
        request.data = request.get_json()
        return (payment_searching(request.data)), 200
    except Exception as e:
        logger.error(f'Error in finance_payments_search POST: {e}')
        return f'Error in finance_payments POST: {e}', 500


@app.route('/finance/order_payments', methods=['POST'])
def fin_pay_order():
    try:
        request.data = request.get_json()
        if 'id_order' in request.data:
            return (payment_id_order_searching(request.data)), 200
        else:
            return ({"message": "order_payments is error"}), 500
    except Exception as e:
        logger.error(f'Error in finance_payments_order POST: {e}')
        return f'Error in order_payments POST: {e}', 500


@app.route('/finance/methods', methods=['GET'])
def fin_met():
    try:
        full_block = {"metod_payment": ["iban", "cash"],
                      "outlay_class": [
                        "податок", "мат. осн.", "мат. доп.",
                        "інстр.", "опл. роб.", "реклама", "інше"],
                      "filter_class": [
                        "day", "week", "month", "quarter", "year"]}
        return (full_block)
    except Exception as e:
        logger.error(f'Error in finance_methods GET: {e}')
        return f'Error in finance_methods GET: {e}', 500


@app.route('/finance/payments', methods=['GET'])
def fin_pay():
    try:
        return (opening_last_payments()), 200
    except Exception as e:
        logger.error(f'Error in finance_payments GET: {e}')
        return f'Error in finance_payments GET: {e}', 500


@app.route('/finance/outlays', methods=['GET'])
def fin_out():
    try:
        return (opening_last_outlays()), 200
    except Exception as e:
        logger.error(f'Error in finance_outlays GET: {e}')
        return f'Error in finance_outlays GET: {e}', 500


@app.route('/finance/payment', methods=['POST'])
def finance_payment():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return (creating_payment(request.data)), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/payment/<int:id>', methods=['PUT'])
def finance_payment_change(id):
    try:
        if request.method == 'PUT':
            request.data = request.get_json()
            return (payment_changing(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/outlay', methods=['POST'])
def finance_outlay():
    request.data = request.get_json()
    try:
        if request.method == 'POST':
            return (creating_outlay(request.data)), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/outlay/<int:id>', methods=['PUT'])
def finance_outlay_changing(id):
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (outlay_changing(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500
