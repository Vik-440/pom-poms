from flask import Flask,jsonify,request
import json
from datetime import datetime, timedelta

from sqlalchemy import false
from _1_main_json import return_data_from_mainpage
from _2_new_order_json import return_data_from_new_order, return_data_from_new_order_post
from _3_material_json import return_data_from_material, return_data_from_material_one, \
    return_data_from_material_change, return_data_from_material_new, return_data_from_material_change_full
from _4_finance_json import return_data_from_finance, return_data_from_payment,return_data_from_outlay, \
    return_data_from_payment_search, return_data_from_outlay_search, return_data_from_payment_change, \
    return_data_from_outlay_change, return_data_from_payment_id_order, return_data_from_payment_stat, \
    return_data_from_payment_balans
from _1_main_page_json import return_data_from_main_page

app =   Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#########################################################################################  
@app.route('/')
def return_data_from_flask ():

    info = {
        "id_order": 541,
        "data_order": "2022-02-23",
        "kolor_model": "малиновий",
        "kod_model": "190-B05"}

    return jsonify(info) # returning a JSON response
#########################################################################################
@app.route('/main_page', methods=['GET', 'POST'])
def main_page ():
    response.headers.add("Access-Control-Allow-Origin", "*")
    if request.method == 'POST':
        request.data = request.get_json()
        return(return_data_from_main_page(request.data))
    # ds=datetime.today().strftime('%Y-%m-%d')
    data={"data_start": "2016-01-01"}#, "data_end" : ds, "fulfilled_order":false}
    return(return_data_from_main_page(data))
#########################################################################################
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage ():
    if request.method == 'POST':
        request.data = request.get_json()
        if 'data_start' in request.data and 'data_end' in request.data:
            data_start_order = request.data['data_start']
            data_end_order = request.data['data_end']
            data = return_data_from_mainpage(data_start_order, data_end_order)
        else:
            data = request.data
        return data
    else: return (return_data_from_mainpage(0,0))
#########################################################################################
@app.route('/new_order', methods=['GET', 'POST'])
def new_order ():
    if request.method == 'POST':
        request.data = request.get_json()
        data=return_data_from_new_order_post(request.data)
        return data
    else: return (return_data_from_new_order())
#########################################################################################
@app.route('/material', methods=['GET', 'POST'])
def material ():
    if request.method == 'POST':
        request.data = request.get_json()
        if 'id_color' in request.data:
            tmp_id_color=request.data['id_color']
            if tmp_id_color == 999:
                data=return_data_from_material(999)
            else:
                data=return_data_from_material_one(request.data)
        elif 'color_new' in request.data:
            data=return_data_from_material_new(request.data)
        elif 'color_change' in request.data:
            data=return_data_from_material_change(request.data)
        elif 'color_change_full' in request.data:
            data=return_data_from_material_change_full(request.data)
        else:
            data={"запит ":"не вірний"}
        # data={"testdata" : "Test-POST-OK"}
        return data
    else:
        return(return_data_from_material(0))
#########################################################################################
@app.route('/finance', methods=['GET', 'POST'])
def finance ():
    if request.method == 'POST':
        request.data = request.get_json()
        if type(request.data) is list:
            if 'payment_group' in request.data[0]:
                return (return_data_from_payment(request.data))
            if 'outlay_group' in request.data[0]:
                return (return_data_from_outlay(request.data))
        elif type(request.data) is dict:
            if 'payment_search' in request.data:
                return (return_data_from_payment_search(request.data))
            if 'outlay_search' in request.data:
                return (return_data_from_outlay_search(request.data))
            if 'id_payment' in request.data:
                return (return_data_from_payment_change(request.data))
            if 'id_outlay' in request.data:
                return (return_data_from_outlay_change(request.data))
            if 'id_order' in request.data:
                return (return_data_from_payment_id_order(request.data))
            if 'stat' in request.data:
                return (return_data_from_payment_stat(request.data))    
            if 'balans' in request.data:
                return (return_data_from_payment_balans(request.data))
        return({"testdata" : "Test-POST-NOT-OK"})
    else:
        return(return_data_from_finance(0))
#########################################################################################
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)