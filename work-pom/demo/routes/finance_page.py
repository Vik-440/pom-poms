from flask import request
from app import app

from functions.finance.finance_crate_data import (
    return_data_from_payment,
    return_data_from_outlay)
from functions.finance.finance_change_data import (
    return_data_from_payment_change,
    return_data_from_outlay_change)
from functions.finance.finance_statistics import (
    return_data_from_payment_stat,
    return_data_from_payment_balans)
from functions.finance.finance_search_filter import (
    return_data_from_payment_search,
    return_data_from_outlay_search,
    return_data_from_payment_id_order)
from functions.finance.finance_start_requests import (
    ret_dat_fin_pay_get,
    ret_dat_fin_out_get)
from log.logger import logger


@app.route('/finance', methods=['GET', 'POST'])
def finance():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            if 'outlay_search' in request.data:
                return (return_data_from_outlay_search(request.data)), 200
            if 'stat' in request.data:
                return (return_data_from_payment_stat(request.data)), 200
            return ({"testdata": "Test-POST-error"}), 500
        else:
            return ({"Finance": "error"}), 500
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/payments/statics', methods=['POST'])
def fin_pay_balans():
    try:
        request.data = request.get_json()
        if 'balans' in request.data:
            return (return_data_from_payment_balans(request.data)), 200
    except Exception as e:
        logger.error(f'Error in finance_payments_balans POST: {e}')
        return f'Error in finance_payments GET: {e}', 500


@app.route('/finance/payments', methods=['POST'])
def fin_pay_search():
    try:
        request.data = request.get_json()
        return (return_data_from_payment_search(request.data)), 200
    except Exception as e:
        logger.error(f'Error in finance_payments_search POST: {e}')
        return f'Error in finance_payments GET: {e}', 500


@app.route('/finance/order_payments', methods=['POST'])
def fin_pay_order():
    try:
        request.data = request.get_json()
        if 'id_order' in request.data:
            return (return_data_from_payment_id_order(request.data)), 200
    except Exception as e:
        logger.error(f'Error in finance_payments_order POST: {e}')
        return f'Error in finance_payments GET: {e}', 500


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
        return (ret_dat_fin_pay_get()), 200
    except Exception as e:
        logger.error(f'Error in finance_payments GET: {e}')
        return f'Error in finance_payments GET: {e}', 500


@app.route('/finance/outlays', methods=['GET'])
def fin_out():
    try:
        return (ret_dat_fin_out_get()), 200
    except Exception as e:
        logger.error(f'Error in finance_outlays GET: {e}')
        return f'Error in finance_outlays GET: {e}', 500


@app.route('/finance/payment', methods=['POST'])
def finance_payment():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return (return_data_from_payment(request.data)), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/payment/<int:id>', methods=['PUT'])
def finance_payment_change(id):
    try:
        if request.method == 'PUT':
            request.data = request.get_json()
            return (return_data_from_payment_change(id, request.data)), 200
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
            return (return_data_from_outlay(request.data)), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500


@app.route('/finance/outlay/<int:id>', methods=['PUT'])
def finance_outlay_change(id):
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (return_data_from_outlay_change(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500
