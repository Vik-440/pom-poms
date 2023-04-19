import pytest
from flask import json


# @pytest.mark.run(order=720010)
# def test_read_order_withot_id_product(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/order', content_type='application/json')
#     assert response.status_code == 405
#     expected_data = '405 METHOD NOT ALLOWED'
#     assert expected_data in str(response)


# @pytest.mark.run(order=420020)
# def test_read_not_int_id_order(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/order/abc', content_type='application/json')
#     assert response.status_code == 404
#     expected_data = '404 NOT FOUND'
#     assert expected_data in str(response)


# @pytest.mark.run(order=420030)
# def test_read_unrial_id_order_get(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/order/10')
#     assert response.status_code == 400
#     expected_data = {'id_order': 'ID order 10 is not exist'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420040)
# def test_read_unrial_id_order_put(app_fixture):
#     client = app_fixture.test_client()
#     data = {'test': 'test'}
#     response = client.put('/order/10')
#     assert response.status_code == 400
#     expected_data = {'id_order': 'ID order 10 is not exist'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420050)
# def test_post_json_not_correct_order(app_fixture):
#     client = app_fixture.test_client()
#     data = 'this is not valid json'
#     response = client.post('/order', data=data)
#     assert response.status_code == 400
#     expected_data = {'order': 'json format is not correct'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420060)
# def test_put_json_not_correct_order(app_fixture):
#     client = app_fixture.test_client()
#     data = 'this is not valid json'
#     response = client.put('/order/1', data=data)
#     assert response.status_code == 400
#     expected_data = {'order': 'json format is not correct'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420070)
# def test_order_without_date_create(app_fixture):
#     client = app_fixture.test_client()
#     data = {
#         # 'date_create': '2023-03-03',
#         'date_plane_send': '2023-03-13',
#         'id_client': 1,
#         'id_recipient': 1,
#         'status_order': False,
#         'sum_payment': 1200,
#         'discount': 0,
#         'comment': None,
#         'id_models': [1],
#         'qty_pars': [3],
#         'price_model_sell': [400],
#         'phase_1': [6],
#         'phase_2': [6],
#         'phase_3': [3]}
#     response = client.post('/order', data=json.dumps(data))
#     assert response.status_code == 400
#     expected_data = {'date_create':  'miss in data'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420080)
# def test_order_not_str_date_create(app_fixture):
#     client = app_fixture.test_client()
#     data = {
#         'date_create': ['2023-03-03'],
#         'date_plane_send': '2023-03-13',
#         'id_client': 1,
#         'id_recipient': 1,
#         'status_order': False,
#         'sum_payment': 1200,
#         'discount': 0,
#         'comment': None,
#         'id_models': [1],
#         'qty_pars': [3],
#         'price_model_sell': [400],
#         'phase_1': [6],
#         'phase_2': [6],
#         'phase_3': [3]}
#     response = client.post('/order', data=json.dumps(data))
#     assert response.status_code == 400
#     expected_data = {'date_create': 'is not str type'}
#     assert response.json == expected_data


# @pytest.mark.run(order=420090)
# def test_order_not_format_date_create(app_fixture):
#     client = app_fixture.test_client()
#     data = {
#         'date_create': '2023.03.03',
#         'date_plane_send': '2023-03-13',
#         'id_client': 1,
#         'id_recipient': 1,
#         'status_order': False,
#         'sum_payment': 1200,
#         'discount': 0,
#         'comment': None,
#         'id_models': [1],
#         'qty_pars': [3],
#         'price_model_sell': [400],
#         'phase_1': [6],
#         'phase_2': [6],
#         'phase_3': [3]}
#     response = client.post('/order', data=json.dumps(data))
#     assert response.status_code == 400
#     expected_data = {"date_create": 'is not in format like: yyyy-mm-dd'}
#     assert response.json == expected_data