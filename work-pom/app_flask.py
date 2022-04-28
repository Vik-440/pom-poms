from flask import Flask,jsonify,request
import json
from _1_main_json import return_data_from_mainpage
from _2_new_order_json import return_data_from_new_order, return_data_from_new_order_post
from _3_material_json import return_data_from_material, return_data_from_material_one, \
            return_data_from_material_change


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
        return data
    else:
        data = return_data_from_mainpage(0,0)
        return data

@app.route('/new_order', methods=['GET', 'POST'])
def new_order ():
    if request.method == 'POST':
        request.data = request.get_json()
        data=return_data_from_new_order_post(request.data)
        return data
    else:
        data=return_data_from_new_order()

        return data

@app.route('/material', methods=['GET', 'POST'])
def material ():
    if request.method == 'POST':
        request.data = request.get_json()
        if 'id_color' in request.data:
            tmp_id_color=request.data['id_color']
            if tmp_id_color == 999:
                data=return_data_from_material(tmp_id_color)
            else:
                data=return_data_from_material_one(tmp_id_color)
        elif 'color_change' in request.data:
            data=return_data_from_material_change(request.data)
        else:
            data={"запит" : "не вірний"}


        # data={"testdata" : "Test-POST-OK"}
        return data
    else:
        data=return_data_from_material(0)
        # data={"testdata" : "Test-GET-OK"}
        return data



if __name__=='__main__':
    app.run(debug=True)