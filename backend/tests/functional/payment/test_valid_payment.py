import pytest
from flask import json


@pytest.mark.run(order=500010)
def test_create_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        'id_order': 1,
        'payment': 100,
        'metod_payment': 'iban',
        'data_payment': '2023-03-03'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'payment': 'creating_payment is excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=500020)
def test_read_payment(app_fixture):
    client = app_fixture.test_client()
    data = {'id_order': 1}
    response = client.post('/finance/order_payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-03',
        'id_order': 1,
        'id_payment': 1,
        'metod_payment': 'iban',
        'payment': 100}]
    assert response.json == expected_data


@pytest.mark.run(order=500030)
def test_create_payment_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        'id_order': 2,
        'payment': 200,
        'metod_payment': 'cash',
        'data_payment': '2023-03-05'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'payment': 'creating_payment is excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=500040)
def test_edit_payment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        'id_order': 2,
        'payment': 222,
        'metod_payment': 'cash',
        'data_payment': '2023-03-05'}
    response = client.put('/finance/payment/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'payment': 'payment changing excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=500050)
def test_read_payment_1(app_fixture):
    client = app_fixture.test_client()
    data = {'id_order': 2}
    response = client.post('/finance/order_payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-05',
        'id_order': 2,
        'id_payment': 2,
        'metod_payment': 'cash',
        'payment': 222}]
    assert response.json == expected_data


@pytest.mark.run(order=500060)
def test_create_payment_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_payment': 1,
        'id_order': 3,
        'payment': 300,
        'metod_payment': 'iban',
        'data_payment': '2023-03-07'}
    response = client.post('/finance/payment', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'payment': 'creating_payment is excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=500070)
def test_read_payments_2(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/finance/payments', content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-03',
        'id_order': 1,
        'id_payment': 1,
        'metod_payment': 'iban',
        'payment': 100},
        {
        'data_payment': '2023-03-05',
        'id_order': 2,
        'id_payment': 2,
        'metod_payment': 'cash',
        'payment': 222},
        {
        'id_payment': 3,
        'id_order': 3,
        'payment': 300,
        'metod_payment': 'iban',
        'data_payment': '2023-03-07'}]
    assert response.json == expected_data


@pytest.mark.run(order=500080)
def test_search_payment_iban(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': True,
        'cash': False}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-03',
        'id_order': 1, 'id_payment': 1,
        'method_payment': 'iban',
        'payment': 100}]
    assert response.json == expected_data

@pytest.mark.run(order=500090)
def test_search_payment_cash(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-01',
        'data_end': '2023-03-06',
        'iban': False,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-05',
        'id_order': 2, 'id_payment': 2,
        'method_payment': 'cash',
        'payment': 222}]
    assert response.json == expected_data

@pytest.mark.run(order=500100)
def test_search_payment_all(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-05',
        'data_end': '2023-03-09',
        'iban': True,
        'cash': True}
    response = client.post('/finance/payments', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'data_payment': '2023-03-05',
        'id_order': 2, 'id_payment': 2,
        'method_payment': 'cash',
        'payment': 222
        },{
        'data_payment': '2023-03-07',
        'id_order': 3, 'id_payment': 3,
        'method_payment': 'iban',
        'payment': 300}]
    # print(response.json)
    assert response.json == expected_data