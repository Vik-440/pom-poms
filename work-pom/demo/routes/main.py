from flask import jsonify, request
from app import app
from functions.main_page_json import return_data_from_main_page
from functions.new_order_json import return_data_from_new_order
from functions.new_order_json import return_data_from_new_order_post
from functions.material_json import return_data_from_material
from functions.material_json import return_data_from_material_one
from functions.material_json import return_data_from_material_change
from functions.material_json import return_data_from_material_new
from functions.material_json import return_data_from_material_change_full
from functions.finance_json import return_data_from_finance
from functions.finance_json import return_data_from_payment
from functions.finance_json import return_data_from_outlay
from functions.finance_json import return_data_from_payment_search
from functions.finance_json import return_data_from_outlay_search
from functions.finance_json import return_data_from_payment_change
from functions.finance_json import return_data_from_outlay_change
from functions.finance_json import return_data_from_payment_id_order
from functions.finance_json import return_data_from_payment_stat
from functions.finance_json import return_data_from_payment_balans


@app.route('/')
def return_data_from_flask():
    info = {
        "id_order": 541,
        "data_order": "2022-02-23",
        "kolor_model": "малиновий",
        "kod_model": "190-B05"}

    return jsonify(info), 200  # returning a JSON response


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return(return_data_from_main_page(request.data))
        # ds=datetime.today().strftime('%Y-%m-%d')
        elif request.method == 'GET':
            data = {"data_start": "2016-01-01"}
            return(return_data_from_main_page(data))
        else:
            return ({"request_metod": "error"}), 500
    except Exception as e:
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
            # data={"testdata" : "Test-POST-OK"}
            return data, 200
        else:
            return(return_data_from_material(0)), 200
    except Exception as e:
        return f'Error in function material: {e}', 500


@app.route('/finance', methods=['GET', 'POST'])
def finance():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            if type(request.data) is list:
                pass

            elif type(request.data) is dict:
                if 'payment_search' in request.data:
                    return (return_data_from_payment_search(request.data)), 200
                if 'outlay_search' in request.data:
                    return (return_data_from_outlay_search(request.data)), 200
                if 'id_order' in request.data:
                    return (return_data_from_payment_id_order(request.data))
                if 'stat' in request.data:
                    return (return_data_from_payment_stat(request.data)), 200
                if 'balans' in request.data:
                    return (return_data_from_payment_balans(request.data)), 200
            return({"testdata": "Test-POST-error"}), 500
        elif request.method == 'GET':
            return(return_data_from_finance(0)), 200
        else:
            return ({"Finance": "error"}), 500
    except Exception as e:
        return f'Error in function finance: {e}', 500


@app.route('/finance/payment', methods=['POST'])
def finance_payment():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return (return_data_from_payment(request.data)), 200
    except Exception as e:
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
        return f'Error in function finance: {e}', 500


@app.route('/finance/outlay', methods=['POST'])
def finance_outlay():
    request.data = request.get_json()
    try:
        if request.method == 'POST':
            return (return_data_from_outlay(request.data)), 200
    except Exception as e:
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
        return f'Error in function finance: {e}', 500
