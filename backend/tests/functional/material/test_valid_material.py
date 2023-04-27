import pytest
from flask import json


@pytest.mark.run(order=100010)
def test_create_material_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'name': '77/23 Білий',
        'width': 23,
        'spool_qty': 1,
        'weight': 1111,
        'comment': 'дуже білий',
        'thickness': 36,
        'spool_weight': 150,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 12.623}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    expected_data = {'id_material': 1}
    assert response.json == expected_data


@pytest.mark.run(order=100020)
def test_create_material_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'name': '70/23 Червоний',
        'width': 23,
        'spool_qty': 2,
        'weight': 2222,
        'comment': None,
        'thickness': 36,
        'spool_weight': 111,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 128}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    expected_data = {'id_material': 2}
    assert response.json == expected_data


@pytest.mark.run(order=100030)
def test_create_material_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'name': '75/23 Золотий',
        'width': 23,
        'spool_qty': 0,
        'weight': 0,
        'comment': None,
        'thickness': 36,
        'spool_weight': 160,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 128}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    expected_data = {'id_material': 3}
    assert response.json == expected_data


@pytest.mark.run(order=100040)
def test_read_available_materials(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials')
    assert response.status_code == 200
    expected_data = [{
        'id_material': 1,
        'name': '77/23 Білий',
        'net_weight': 961,
        'spool_qty': 1,
        'width': 23
        }, {
        'id_material': 2,
        'name': '70/23 Червоний',
        'net_weight': 2000,
        'spool_qty': 2,
        'width': 23}]
    # print(response.json)
    assert response.json == expected_data


@pytest.mark.run(order=100050)
def test_read_all_materials(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials?available=all')
    assert response.status_code == 200
    expected_data = [{
        'id_material': 1,
        'name': '77/23 Білий',
        'net_weight': 961,
        'spool_qty': 1,
        'width': 23
        }, {
        'id_material': 2,
        'name': '70/23 Червоний',
        'net_weight': 2000,
        'spool_qty': 2,
        'width': 23
        }, {
        'id_material': 3,
        'name': '75/23 Золотий',
        'net_weight': 0,
        'spool_qty': 0,
        'width': 23}]
    # print(response.json)
    assert response.json == expected_data


@pytest.mark.run(order=100060)
def test_get_one_material(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials/1')
    assert response.status_code == 200
    expected_data = {
        'name': '77/23 Білий',
        'id_material': 1,
        'width': 23,
        'spool_qty': 1,
        'weight': 1111,
        'comment': 'дуже білий',
        'thickness': 36,
        'spool_weight': 150,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 12.62}
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=100070)
def test_chenge_one_material_full(app_fixture):
    client = app_fixture.test_client()
    data = {
        'name': '77/23 Білий',
        'width': 23,
        'spool_qty': 5,
        'weight': 5555,
        'comment': 'дуже білий',
        'thickness': 36,
        'spool_weight': 150,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 12.668}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 202
    expected_data = {'message': "data_change ok"}
    # assert response.json == expected_data
    print(response.json)


@pytest.mark.run(order=100080)
def test_get_one_material_1(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials/1')
    assert response.status_code == 200
    expected_data = {
        'name': '77/23 Білий',
        'id_material': 1,
        'width': 23,
        'spool_qty': 5,
        'weight': 5555,
        'comment': 'дуже білий',
        'thickness': 36,
        'spool_weight': 150,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 12.67}
    assert response.json == expected_data


@pytest.mark.run(order=100090)
def test_chenge_one_material_weight(app_fixture):
    client = app_fixture.test_client()
    data = {
        'edit_spool_qty': -1,
        'edit_weight': -1111}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 202
    expected_data = { "spool_qty": 4, "net_weight": 3844}
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=100100)
def test_get_one_material_2(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials/1')
    assert response.status_code == 200
    expected_data = {
        'name': '77/23 Білий',
        'id_material': 1,
        'width': 23,
        'spool_qty': 4,
        'weight': 4444,
        'comment': 'дуже білий',
        'thickness': 36,
        'spool_weight': 150,
        'manufacturer': 'Ровно',
        'reserve': 0,
        'weight_10m': 12.67}
    assert response.json == expected_data
