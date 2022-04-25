from tracemalloc import stop
from tmp_main import return_data_from_sql
# from app_flask import return_data_from_flask
# from flask import Flask,jsonify,request
# app =   Flask(__name__)
# app.config['JSON_AS_ASCII'] = False


import json
# import codecs
# json.load(codecs.open('sample.json', 'r', 'utf-8-sig'))

def return_data_from_mainpage(data_start_order, data_end_order):

    data = return_data_from_sql(data_start_order, data_end_order)
    # print(data["id_order"])
    # print(data["data_order"])
    # print(data['kolor_model'])
    # print(data['kolor_model_1'])
    # print(data['kod_model'])
    # print(data['kod_model_1'])
    # print(data['quantity_pars_model'])
    # print(data['phase_1_model'])
    # print(data['phase_2_model'])
    # print(data['phase_3_model'])
    # print(data['sity'])
    # print(data['sum_payment'])
    # print(data['real_money'])
    # print(data['data_plane_order'])
    # print(data['comment_order'])
    # print(data['comment_model'])
    # print(data['fulfilled_order'])

    a1a=len(data["id_order"])
    full_block=[]
    # # print(a1a)
    while a1a > 0:
        a1a-=1
        # print(a1a)
        element_1=data['id_order'][0]
        element_2=data["data_order"][0]
        element_3=data['kolor_model'][0]
        del data['id_order'][0]
        del data["data_order"][0]
        del data['kolor_model'][0]
        element_5=data['kod_model'][0]
        del data['kod_model'][0]
        element_7=data['quantity_pars_model'][0]
        del data['quantity_pars_model'][0]
        element_8=data['phase_1_model'][0]
        del data['phase_1_model'][0]
        element_9=data['phase_2_model'][0]
        del data['phase_2_model'][0]
        element_10=data['phase_3_model'][0]
        del data['phase_3_model'][0]
        element_11=data['sity'][0]
        del data['sity'][0]
        element_12=data['sum_payment'][0]
        del data['sum_payment'][0]
        element_13=data['real_money'][0]
        del data['real_money'][0]
        element_14=data['data_plane_order'][0]
        del data['data_plane_order'][0]
        element_15=data['comment_order'][0]
        del data['comment_order'][0]
        element_16=data['comment_model'][0]
        del data['comment_model'][0]
        element_17=data['fulfilled_order'][0]
        del data['fulfilled_order'][0]

        one_block = {'id_order': element_1, 'data_order': element_2, "kolor_model" : element_3, "kod_model" : element_5,
        "comment_model" : element_16, "kolor_cell_model_mat" : 'треба дописати код - модель помпонів',
        "quantity_pars_model" : element_7, "kolor_cell_pars" : 'треба дописати код - наявність матеріалів',
        "phase_1_model" : element_8, "phase_2_model" : element_9, "phase_3_model" : element_10,
        "sum_payment" : element_12, "real_money" : element_13, "sity" : element_11, "data_plane_order" : element_14,
        "fulfilled_order" : element_17, "comment_order" : element_16}

        full_block.append(one_block)


    # to_json = {'id_order': element_1, 'data_order': element_2, "kolor_model" : element_3, "kod_model" : element_5,
    #     "comment_model" : element_16, "kolor_cell_model_mat" : 'треба дописати код - модель помпонів',
    #     "quantity_pars_model" : element_7, "kolor_cell_pars" : 'треба дописати код - наявність матеріалів',
    #     "phase_1_model" : element_8, "phase_2_model" : element_9, "phase_3_model" : element_10,
    #     "sum_payment" : element_12, "real_money" : element_13, "sity" : element_11, "data_plane_order" : element_14,
    #     "fulfilled_order" : element_17, "comment_order" : element_16}

    to_json = full_block

    # with open('sw_templates.json', 'w') as f:
    #     f.write(json.dumps(to_json, indent=4, ensure_ascii=False))

    # with open('sw_templates.json') as f:
    #     print(f.read())
    return json.dumps(to_json, ensure_ascii=False)
    
    # return {}

#'id_order': j_id_order
  
