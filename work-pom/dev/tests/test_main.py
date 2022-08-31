# from starlette.testclient import TestClient
# from app import app
# client = TestClient(app)
import json
from routes.main import tmp_test_tmp
from routes.main import return_data_from_new_order
from routes.main import return_data_from_main_page
from routes.main import fin_met
from routes.main import change_main_phase


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
