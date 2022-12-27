from flask import request  # jsonify
from app import app
from functions.main_page_json import return_data_from_main_page
from functions.main_page_json import change_main_phase
from functions.new_order_json import return_data_from_new_order
from functions.new_order_json import return_data_from_new_order_post
from functions.material_json import return_data_from_material
from functions.material_json import return_data_from_material_one
from functions.material_json import return_data_from_material_change
from functions.material_json import return_data_from_material_new
from functions.material_json import return_data_from_material_change_full
from functions.finance_json import return_data_from_payment
from functions.finance_json import return_data_from_outlay
from functions.finance_json import return_data_from_payment_search
from functions.finance_json import return_data_from_outlay_search
from functions.finance_json import return_data_from_payment_change
from functions.finance_json import return_data_from_outlay_change
from functions.finance_json import return_data_from_payment_id_order
from functions.finance_json import return_data_from_payment_stat
from functions.finance_json import return_data_from_payment_balans
from functions.finance_json import ret_dat_fin_pay_get
from functions.finance_json import ret_dat_fin_out_get
from functions.get_main_json import get_main
from functions.get_main_json import change_phase_order_put
from functions.get_main_json import changing_status_order
from log.logger import logger


@app.route('/log', methods=['GET'])
def get_log():
    with open('pom-poms.log', 'r') as f:
        return f.read()


@app.route('/')
def return_data_from_flask():
    info = {"id_order": 0}
    return (info), 200  # returning a JSON response


def tmp_test_tmp():
    x = {"ping": "pong", "ping_1": "pong_1"}
    return (x)


@app.route('/main', methods=['GET'])
def main():
    try:
        if request.method == 'GET':
            data = request.args
            logger.info('Get main is work!')
            return (get_main(data))
        else:
            return ({"request_metod": "error"}), 500
    except Exception as e:
        logger.error(f'Error in function main: {e}')
        return f'Error in function main: {e}', 500


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return (return_data_from_main_page(request.data))
        # ds=datetime.today().strftime('%Y-%m-%d')
        elif request.method == 'GET':
            data = {"data_start": "2016-01-01"}
            logger.info('Get main_page is work!')
            return (return_data_from_main_page(data))
        else:
            return ({"request_metod": "error"}), 500
    except Exception as e:
        logger.error(f'Error in function mainpage: {e}')
        return f'Error in function mainpage: {e}', 500


@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            data = return_data_from_new_order_post(request.data)
            return data, 200
        else:
            return (return_data_from_new_order())
    except Exception as e:
        logger.error(f'Error in function new_order: {e}')
        return f'Error in function new_order: {e}', 500


@app.route('/material', methods=['GET', 'POST'])
def material():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            if 'id_color' in request.data:
                tmp_id_color = request.data['id_color']
                if tmp_id_color == 999:
                    data = return_data_from_material(999)
                else:
                    data = return_data_from_material_one(request.data)
            elif 'color_new' in request.data:
                data = return_data_from_material_new(request.data)
            elif 'color_change' in request.data:
                data = return_data_from_material_change(request.data)
            elif 'color_change_full' in request.data:
                data = return_data_from_material_change_full(request.data)
            else:
                data = {"запит ": "не вірний"}
            return data, 200
        else:
            return (return_data_from_material(0)), 200
    except Exception as e:
        logger.error(f'Error in function material: {e}')
        return f'Error in function material: {e}', 500


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


@app.route('/main_page/phase/<int:id>', methods=['PUT'])
def main_phase(id):
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (change_main_phase(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function main_phase: {e}')
        return f'Error in function main_phase: {e}', 500


@app.route('/main/phase/<int:id>', methods=['PUT'])
def main_phase_get(id):
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (change_phase_order_put(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function main_phase: {e}')
        return f'Error in function main_phase: {e}', 500


@app.route('/main/status/<int:id>', methods=['PUT'])
def main_status_order(id):
    request.data = request.get_json()
    try:
        return (changing_status_order(id, request.data)), 200
    except Exception as e:
        return f'Error in function main_status_order: {e}', 500
