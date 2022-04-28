from flask import Flask,jsonify,request
import json
from _1_main_json import return_data_from_mainpage
from _2_new_order_json import return_data_from_new_order, return_data_from_new_order_post
from _3_material_json import return_data_from_material


app =   Flask(__name__)
app.config['JSON_AS_ASCII'] = False
  
@app.route('/')
def return_data_from_flask ():

    info = {
        "id_order": 541,
        "data_order": "2022-02-23",
        "kolor_model": "малиновий",
        "kod_model": "190-B05"}

    return jsonify(info) # returning a JSON response






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

        # return jsonify(info_1) # returning a JSON response
        # return request.data
        return data
    else:
        data = return_data_from_mainpage(0,0)
        # with open('sw_templates.json') as f:
        #     info = f.read()
        return data # returning a JSON response

@app.route('/new_order', methods=['GET', 'POST'])
def new_order ():
    if request.method == 'POST':
        request.data = request.get_json()
        data=return_data_from_new_order_post(request.data)
        # print(request.data)
        # data={"testdata" : "Test-OK"}
        return data
    else:                           ######## потрібновіддати: Номер наступного ордеру, дата зайнятої черги.
        # request.data = request.get_json()
        data=return_data_from_new_order()
        # data_json = {"id_new_order":data['id_new_order'], "time_last_order":data['time_last_order']}
        # return data_json # returning a JSON response
        return data

@app.route('/material', methods=['GET', 'POST'])
def material ():
    if request.method == 'POST':
        # request.data = request.get_json()
        # data=return_data_from_new_order_post(request.data)
        data={"testdata" : "Test-POST-OK"}
        return data
    else:                           ######## потрібновіддати: Номер наступного ордеру, дата зайнятої черги.
        data=return_data_from_material(0)
        # data={"testdata" : "Test-GET-OK"}
        return data



if __name__=='__main__':
    app.run(debug=True)