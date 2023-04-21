import pytest
from flask import json


@pytest.mark.run(order=520010)
def test_read_payment_withot_id_payment(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/finance/payment', content_type='application/json')
    assert response.status_code == 405
    expected_data = '405 METHOD NOT ALLOWED'
    assert expected_data in str(response)


@pytest.mark.run(order=520020)
def test_post_json_not_correct_payment(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance/payment', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'payment(POST)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=520021)
def test_post_json_not_correct_payment_1(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/finance/payment/1', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'payment(PUT)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=520022)
def test_post_json_not_correct_payment_2(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance/order_payments', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'order_payments(POST)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=520030)
def test_post_without_id_order_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        # 'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520040)
def test_post_id_order_not_int_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': '1',
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=520050)
def test_post_id_order_not_real_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 100,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 100 is not real'}
    assert response.json == expected_data


@pytest.mark.run(order=520050)
def test_post_id_order_closed_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 4,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 4 is closed'}
    assert response.json == expected_data


@pytest.mark.run(order=520060)
def test_post_without_payment_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        # 'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'payment': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520070)
def test_post_payment_not_int_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': '100',
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'payment': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=520080)
def test_post_without_metod_payment_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        # 'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'metod_payment': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520090)
def test_post_metod_payment_not_str_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        'metod_payment': ['iban'],
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'metod_payment': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=520100)
def test_post_metod_payment_not_valid_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        'metod_payment': 'test',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'metod_payment': 'method is not valid'}
    assert response.json == expected_data


@pytest.mark.run(order=520110)
def test_post_without_date_payment_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        # 'data_payment': '2023-03-03'
        }
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_payment': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520120)
def test_post_data_payment_not_str_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': ['2023-03-03']}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_payment': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=520130)
def test_post_data_payment_not_valid_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023.03.03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_payment': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=520140)
def test_post_without_id_order_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        # 'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.put('/finance/payment/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'miss in data'}
    assert response.json == expected_data

@pytest.mark.run(order=520150)
def test_post_without_date_start_search_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520160)
def test_post_date_start_search_payment_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': ['2023-03-01'],
        'data_end': '2023-03-06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=520170)
def test_post_date_start_search_payment_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023.03.01',
        'data_end': '2023-03-06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data

@pytest.mark.run(order=520180)
def test_post_without_date_end_search_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        # 'data_end': '2023-03-06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520190)
def test_post_date_end_search_payment_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': ['2023-03-06'],
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=520200)
def test_post_date_end_search_payment_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023.03.06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=520210)
def test_post_search_payment_without_iban(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        # 'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'iban': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520220)
def test_post_search_payment_iban_not_bool(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': 'False',
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'iban': 'is not bool type'}
    assert response.json == expected_data

@pytest.mark.run(order=520230)
def test_post_search_payment_without_cash(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': False,
        # 'cash': True
        }
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'cash': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=520240)
def test_post_search_payment_cash_not_bool(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': False,
        'cash': 'True'}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'cash': 'is not bool type'}
    assert response.json == expected_data

@pytest.mark.run(order=520250)
def test_post_json_not_correct_search_payment(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance/payments', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'search_payments(POST)': 'json format is not correct'}
    assert response.json == expected_data