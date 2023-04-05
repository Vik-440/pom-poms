import pytest
from flask import json


@pytest.mark.run(order=400010)
def test_create_order(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_order': 1,
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
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.post('/order', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'id_order': 1}
    assert response.json == expected_data


@pytest.mark.run(order=400020)
def test_read_order_1(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/order/1', content_type='application/json')
    expected_data = {
        'id_order': 1,
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
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=400030)
def test_edit_order(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_order': 1,
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-23',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': 'test',
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    response = client.put('/order/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'edit_order': 1}
    assert response.json == expected_data


@pytest.mark.run(order=400040)
def test_read_order_2(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/order/1', content_type='application/json')
    expected_data = {
        'id_order': 1,
        'date_create': '2023-03-03',
        'date_plane_send': '2023-03-23',
        'id_client': 1,
        'id_recipient': 1,
        'status_order': False,
        'sum_payment': 1200,
        'discount': 0,
        'comment': 'test',
        'id_models': [1],
        'qty_pars': [3],
        'price_model_sell': [400],
        'phase_1': [6],
        'phase_2': [6],
        'phase_3': [3]}
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=400050)
def test_create_order_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_order': 1,
        'date_create': '2023-03-05',
        'date_plane_send': '2023-03-25',
        'id_client': 2,
        'id_recipient': 2,
        'status_order': False,
        'sum_payment': 4200,
        'discount': 0,
        'comment': 'test',
        'id_models': [2, 3, 4],
        'qty_pars': [3, 6, 1],
        'price_model_sell': [400, 400, 420],
        'phase_1': [6, 12, 2],
        'phase_2': [6, 12, 2],
        'phase_3': [3, 6, 1]}
    response = client.post('/order', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'id_order': 2}
    assert response.json == expected_data


@pytest.mark.run(order=400060)
def test_create_order_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_order': 1,
        'date_create': '2023-03-07',
        'date_plane_send': '2023-03-27',
        'id_client': 1,
        'id_recipient': 2,
        'status_order': False,
        'sum_payment': 11440,
        'discount': 0,
        'comment': 'test',
        'id_models': [5, 9],
        'qty_pars': [11, 22],
        'price_model_sell': [400, 320],
        'phase_1': [22, 44],
        'phase_2': [22, 44],
        'phase_3': [11, 22]}
    response = client.post('/order', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'id_order': 3}
    assert response.json == expected_data