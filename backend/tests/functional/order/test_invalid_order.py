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
    response = client.post('/order', data=json.dumps(data), content_type='application/json')
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


@pytest.mark.run(order=420120)
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


@pytest.mark.run(order=420280)
def test_order_without_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        # 'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_models':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420290)
def test_order_not_list_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': 1,
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_models': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420300)
def test_order_empty_list_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_models': 'is empty'}
    assert response.json == expected_data


@pytest.mark.run(order=420310)
def test_order_not_int_in_list_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [5, '123', 1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_models': '123 is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420320)
def test_order_not_real_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [5, 51],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'id_models': 'ID product 51 is not real'}
    assert response.json == expected_data


@pytest.mark.run(order=420330)
def test_order_without_qty_pars(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        # 'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'qty_pars':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420340)
def test_order_not_list_qty_pars(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1],
        'qty_pars': 3,
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'qty_pars': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420350)
def test_order_not_correct_qty_pars(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'qty_pars': 'qty positions in qty_pars is not eiqual qty in id_models'}
    assert response.json == expected_data


@pytest.mark.run(order=420360)
def test_order_not_int_in_list_qty_pars(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [1, '3'],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'qty_pars': '3 in qty_pars is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420370)
def test_order_without_phase_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
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
        # 'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_1':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420380)
def test_order_not_list_phase_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
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
        'phase_1': 6,
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_1': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420390)
def test_order_not_correct_phase_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_1': 'qty positions in phase_1 is not eiqual qty in id_models'}
    assert response.json == expected_data


@pytest.mark.run(order=420400)
def test_order_not_int_in_list_phase_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, '5'],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_1': '5 in phase_1 is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420410)
def test_order_list_phase_1_bigger_then_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 15],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_1': '15 in phase_1 is bigger then it is possible (qty_pars * 2)'}
    assert response.json == expected_data


@pytest.mark.run(order=420420)
def test_order_without_phase_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        # 'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_2':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420430)
def test_order_not_list_phase_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': 6,
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_2': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420440)
def test_order_not_correct_phase_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_2': 'qty positions in phase_2 is not eiqual qty in id_models'}
    assert response.json == expected_data


@pytest.mark.run(order=420450)
def test_order_not_int_in_list_phase_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, '5'],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_2': '5 in phase_2 is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420460)
def test_order_list_phase_2_bigger_then_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 15],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_2': '15 in phase_2 is bigger then it is possible (qty_pars * 2)'}
    assert response.json == expected_data


@pytest.mark.run(order=420470)
def test_order_without_phase_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        # 'phase_3': [3]
        }
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_3':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420480)
def test_order_not_list_phase_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': 3}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_3': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420490)
def test_order_not_correct_phase_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_3': 'qty positions in phase_3 is not eiqual qty in id_models'}
    assert response.json == expected_data


@pytest.mark.run(order=420500)
def test_order_not_int_in_list_phase_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, '5']}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_3': '5 in phase_3 is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=420510)
def test_order_list_phase_3_bigger_then_id_models(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, 15]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'phase_3': '15 in phase_3 is bigger then it is possible (qty_pars)'}
    assert response.json == expected_data


@pytest.mark.run(order=420520)
def test_order_without_price_model_sell(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        # 'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, 5]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'price_model_sell':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=420530)
def test_order_not_list_price_model_sell(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': 400,
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, 5]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'price_model_sell': 'is not list type'}
    assert response.json == expected_data


@pytest.mark.run(order=420540)
def test_order_not_correct_price_model_sell(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, 5]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'price_model_sell': 'qty positions in price_model_sell is not eiqual qty in id_models'}
    assert response.json == expected_data


@pytest.mark.run(order=420550)
def test_order_not_int_in_list_price_model_sell(app_fixture):
    client = app_fixture.test_client()
    data = {
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-13',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': None,
        'id_models': [1, 3],
        'qty_pars': [3, 5],
        'price_model_sell': [400, '5'],
        'phase_1': [6, 10],
        'phase_2': [6, 10],
        'phase_3': [3, 5]}
    response = client.post('/order', data=json.dumps(data))
    assert response.status_code == 400
    expected_data = {'price_model_sell': '5 in price_model_sell is not int type'}
    assert response.json == expected_data