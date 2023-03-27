# for start testing use: pytest -rA

# from starlette.testclient import TestClient
# from app import app
# client = TestClient(app)
import json
# from urllib import response
from routes.main import tmp_test_tmp
from routes.main import return_data_from_new_order
from routes.main import return_data_from_main_page
from routes.main import fin_met
from routes.main import change_main_phase
from app import app
# from flask import json


def test_ziro():
    response = app.test_client().get('/')
    origin_data = {"id_order": 0}
    origin_data_1 = 0
    test_data = json.loads(response.data)
    test_data_1 = test_data['id_order']
    assert response.status_code == 200
    assert test_data == origin_data
    assert test_data_1 == origin_data_1


def test_get_main_json_flask():
    response = app.test_client().get(
        'main?data_start=2016-06-15&fulfilled=all&data_finish=2016-06-15')
    test_data_0 = ((response.get_data(as_text=True)).replace(
        "[", "").replace("]", ""))

    test_data = json.loads(test_data_0)

    assert response.status_code == 200
    assert (test_data["comment_model"]) is None
    assert (test_data["comment_order"]) == ""
    assert (test_data["data_order"]) == "2016-06-15"
    assert (test_data["first_name_client"]) == "Ольга"
    assert (test_data["fulfilled_order"]) is True
    assert (test_data["id_order"]) == 0
    assert (test_data["kod_model"]) == "190-12"
    assert (test_data["kolor_model"]) == "Червоний"
    assert (test_data["phase_1"]) == 0
    assert (test_data["phase_2"]) == 0
    assert (test_data["phase_3"]) == 0
    assert (test_data["phone_client"]) == "380631756435"
    assert (test_data["phone_recipient"]) == "380631756435"
    assert (test_data["quantity_pars_model"]) == 3
    assert (test_data["real_money"]) == 450
    assert (test_data["second_name_client"]) == "Коробенко"
    assert (test_data["sity"]) == "Самовивіз"
    assert (test_data["sum_payment"]) == 450
    assert (test_data["zip_code"]) is None


def test_main_page_get_flask():
    response = app.test_client().post('/main_page', data=json.dumps(
        {"data_start": "2016-06-15", "data_end": "2016-06-15",
         "fulfilled_order": False}), content_type='application/json')
    test_data_0 = ((response.get_data(as_text=True)).replace(
        "[", "").replace("]", ""))
    test_data = json.loads(test_data_0)
    # print(test_data)
    assert response.status_code == 200
    assert (test_data["comment_model"]) is None
    assert (test_data["comment_order"]) == ""
    assert (test_data["data_order"]) == "2016-06-15"
    assert (test_data["first_name_client"]) == "Ольга"
    assert (test_data["fulfilled_order"]) is True
    assert (test_data["id_order"]) == 0
    assert (test_data["kod_model"]) == "190-12"
    assert (test_data["kolor_model"]) == "Червоний"
    assert (test_data["phase_1"]) == 0
    assert (test_data["phase_2"]) == 0
    assert (test_data["phase_3"]) == 0
    assert (test_data["phone_client"]) == "380631756435"
    assert (test_data["phone_recipient"]) == "380631756435"
    assert (test_data["quantity_pars_model"]) == 3
    assert (test_data["real_money"]) == 450
    assert (test_data["second_name_client"]) == "Коробенко"
    assert (test_data["sity"]) == "Самовивіз"
    assert (test_data["sum_payment"]) == 450
    assert (test_data["zip_code"]) is None


def test_ping_pong():
    info = {"ping": "pong", "ping_1": "pong_1"}
    assert info == tmp_test_tmp()


def test_new_order_get():
    origin_data = ['id_new_order', 'time_last_order']
    test_data = return_data_from_new_order()
    for x in origin_data:
        assert x in test_data


def test_main_page_get():
    origin_data = ["id_order", "comment_order", "data_order", "kolor_model",
                   "kod_model", "comment_model", "quantity_pars_model",
                   "phase_1_model", "phase_2_model", "phase_3_model",
                   "phase_1", "phase_2", "phase_3", "sum_payment",
                   "real_money", "phone_client", "phone_recipient", "sity",
                   "data_plane_order", "fulfilled_order", "np_number",
                   "zip_code", "street_house_apartment", "second_name_client",
                   "first_name_client"]
    data = {"data_start": "2016-01-01"}
    test_data = return_data_from_main_page(data)
    for x in origin_data[0]:
        assert x in test_data


def test_finanse_start_param_get():
    origin_data = ["metod_payment", "outlay_class", "filter_class"]
    test_data = fin_met()
    for x in origin_data:
        assert x in test_data


def test_int_phasa_change():
    post_data_out = {"data_start": "2016-06-15", "data_end": "2016-06-15",
                     "fulfilled_order": False}
    test_data = (return_data_from_main_page(post_data_out))
    test_data_rep1 = test_data.replace("[", " ")
    test_data_rep = test_data_rep1.replace("]", " ")
    test_data_dict = json.loads((test_data_rep))
    test_phase_1 = (test_data_dict['phase_1'])
    test_phase_2 = (test_data_dict['phase_2'])
    test_phase_3 = (test_data_dict['phase_3'])
    assert test_phase_1 == 0
    assert test_phase_2 == 0
    assert test_phase_3 == 0
    data = {"phase_1": [1]}
    test_data_phase = change_main_phase(0, data)
    assert (test_data_phase['check_sum_phase']) == 1
    post_data_out = {"data_start": "2016-06-15", "data_end": "2016-06-15",
                     "fulfilled_order": False}
    test_data = (return_data_from_main_page(post_data_out))
    test_data_rep1 = test_data.replace("[", " ")
    test_data_rep = test_data_rep1.replace("]", " ")
    test_data_dict = json.loads((test_data_rep))
    test_phase_1 = (test_data_dict['phase_1'])
    assert test_phase_1 == 1

    data = {"phase_1": [0]}
    test_data_phase = change_main_phase(0, data)
    assert (test_data_phase['check_sum_phase']) == 0
    post_data_out = {"data_start": "2016-06-15", "data_end": "2016-06-15",
                     "fulfilled_order": False}
    test_data = (return_data_from_main_page(post_data_out))
    test_data_rep1 = test_data.replace("[", " ")
    test_data_rep = test_data_rep1.replace("]", " ")
    test_data_dict = json.loads((test_data_rep))
    test_phase_1 = (test_data_dict['phase_1'])
    assert test_phase_1 == 0


def test_int_phasa_change_flask():
    ask_get = 'main?data_start=2016-06-15&fulfilled=all&data_finish=2016-06-15'
    test_data = decode_get_answer(ask_get)
    assert test_data['phase_1'] == 0
    assert test_data['phase_2'] == 0
    assert test_data['phase_3'] == 0

    data_chenge = {"phase_1": [1]}
    test_data = decode_put_answer(data_chenge)
    assert (test_data['check_sum_phase']) == 1

    test_data = decode_get_answer(ask_get)
    assert test_data['phase_1'] == 1

    data_chenge = {"phase_1": [0]}
    test_data = decode_put_answer(data_chenge)
    assert (test_data['check_sum_phase']) == 0

    test_data = decode_get_answer(ask_get)
    assert test_data['phase_1'] == 0


def gettig_data_by_flask_get(response: str) -> dict:
    test_data_0 = ((response.get_data(as_text=True)).replace(
        "[", "").replace("]", ""))
    test_data = json.loads(test_data_0)
    return test_data


def decode_get_answer(ask_get: str) -> str:
    response = app.test_client().get(ask_get)
    test_data = gettig_data_by_flask_get(response)
    return test_data


def decode_put_answer(data_chenge: dict) -> str:
    response = app.test_client().put('/main/phase/0', data=json.dumps(
        data_chenge), content_type='application/json')
    test_data = gettig_data_by_flask_get(response)
    return test_data
