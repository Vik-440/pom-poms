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
    response = client.post('/finance/payment', data=data)
    assert response.status_code == 400
    expected_data = {'payment(POST)': 'json format is not correct'}
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



# @pytest.mark.run(order=520020)
# def test_read_not_int_id_order(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/order/abc', content_type='application/json')
#     assert response.status_code == 404
#     expected_data = '404 NOT FOUND'
#     assert expected_data in str(response)


# @pytest.mark.run(order=520030)
# def test_read_unrial_id_order_get(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/order/10')
#     assert response.status_code == 400
#     expected_data = {'id_order': 'ID order 10 is not exist'}
#     assert response.json == expected_data