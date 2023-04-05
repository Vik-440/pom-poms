import pytest
from flask import json


@pytest.mark.run(order=420010)
def test_read_order_withot_id_product(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/order', content_type='application/json')
    assert response.status_code == 405
    expected_data = '405 METHOD NOT ALLOWED'
    assert expected_data in str(response)


@pytest.mark.run(order=420020)
def test_read_not_int_id_order(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/order/abc', content_type='application/json')
    assert response.status_code == 404
    expected_data = '404 NOT FOUND'
    assert expected_data in str(response)


@pytest.mark.run(order=420030)
def test_read_unrial_id_order_get(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/order/10')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 10 is not exist'}
    assert response.json == expected_data


@pytest.mark.run(order=420040)
def test_read_unrial_id_order_put(app_fixture):
    client = app_fixture.test_client()
    data = {'test': 'test'}
    response = client.put('/order/10')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 10 is not exist'}
    assert response.json == expected_data


@pytest.mark.run(order=420050)
def test_post_json_not_correct_order(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/order', data=data)
    assert response.status_code == 400
    expected_data = {'order': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=420060)
def test_put_json_not_correct_order(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/order/1', data=data)
    assert response.status_code == 400
    expected_data = {'order': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=420070)
def test_order_without_date_create(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'date_create':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420080)
def test_order_not_str_date_create(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': ['2023-03-03'],
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'date_create': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=420090)
def test_order_not_format_date_create(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023.03.03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {"date_create": 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=420100)
def test_order_future_date_create(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2053-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {"date_create": 'date future -> misstake'}
    assert response.json == expected_data


@pytest.mark.run(order=420110)
def test_order_without_date_plane_send(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        # 'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'date_plane_send':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420120)
def test_order_not_str_date_plane_send(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': ('2023-03-13',),
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'date_plane_send': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=420130)
def test_order_not_format_date_plane_send(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023/03/13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {"date_plane_send": 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=420140)
def test_order_without_id_client(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        # 'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_client':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420150)
def test_order_not_int_id_client(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': '1',
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_client': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420160)
def test_order_unreal_id_client(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 100,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_client': 'ID is not real'}
    assert response.json == expected_data


@pytest.mark.run(order=420170)
def test_order_without_id_recipient(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        # 'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_recipient':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420180)
def test_order_not_int_id_recipient(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': '1',
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_recipient': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420190)
def test_order_unreal_id_recipient(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 100,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_recipient': 'ID is not real'}
    assert response.json == expected_data


@pytest.mark.run(order=4201200)
def test_order_without_status_order(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        # 'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'status_order':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420210)
def test_order_not_bool_status_order(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': 'False',
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'status_order': 'is not bool type'}
    assert response.json == expected_data


@pytest.mark.run(order=420220)
def test_order_without_sum_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        # 'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'sum_payment':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420230)
def test_order_not_int_sum_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': [1200],
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'sum_payment': 'is not int type'}
    assert response.json == expected_data

@pytest.mark.run(order=420240)
def test_order_without_discount(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        # 'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'discount':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420250)
def test_order_not_int_discount(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': None,
        'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'discount': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420260)
def test_order_without_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        # 'comment': None,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'comment':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420270)
def test_order_not_str_none_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': 123,
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'comment': 'is not str or None type'}
    assert response.json == expected_data