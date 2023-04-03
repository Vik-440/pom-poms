import pytest
from flask import json


@pytest.mark.run(order=100010)
def test_create_material_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_new': 0,
        'name_color': '77/23 Білий',
        'width_color': 23,
        'bab_quantity_color': 1,
        'weight_color': 1111,
        'comment_color': 'дуже білий',
        'thickness_color': 36,
        'bab_weight_color': 150,
        'manufacturer_color': 'Ровно',
        'reserve_color': 0,
        'weight_10m_color': 126}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json['id_color'] == 1


@pytest.mark.run(order=100020)
def test_create_material_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_new': 0,
        'name_color': '70/23 Червоний',
        'width_color': 23,
        'bab_quantity_color': 2,
        'weight_color': 2222,
        'comment_color': '',
        'thickness_color': 36,
        'bab_weight_color': 111,
        'manufacturer_color': 'Ровно',
        'reserve_color': 0,
        'weight_10m_color': 128}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json['id_color'] == 2


@pytest.mark.run(order=100030)
def test_create_material_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_new': 0,
        'name_color': '75/23 Золотий',
        'width_color': 23,
        'bab_quantity_color': 0,
        'weight_color': 0,
        'comment_color': '',
        'thickness_color': 36,
        'bab_weight_color': 160,
        'manufacturer_color': 'Ровно',
        'reserve_color': 0,
        'weight_10m_color': 128}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json['id_color'] == 3


@pytest.mark.run(order=100040)
def test_get_available_materials(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/material')
    assert response.status_code == 200
    expected_data = [
        {
        'bab_quantity_color': 1,
        'comment_color': 'дуже білий',
        'id_color': 1,
        'name_color': '77/23 Білий',
        'weight_color': 961,
        'width_color': 23
        },
        {
        'bab_quantity_color': 2,
        'comment_color': '',
        'id_color': 2,
        'name_color': '70/23 Червоний',
        'weight_color': 2000,
        'width_color': 23}]
    assert response.json == expected_data


@pytest.mark.run(order=100050)
def test_get_all_materials(app_fixture):
    client = app_fixture.test_client()
    data = {'id_color': 999}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = [
        {
        'bab_quantity_color': 1,
        'comment_color': 'дуже білий',
        'id_color': 1,
        'name_color': '77/23 Білий',
        'weight_color': 961,
        'width_color': 23
        },
        {
        'bab_quantity_color': 2,
        'comment_color': '',
        'id_color': 2,
        'name_color': '70/23 Червоний',
        'weight_color': 2000,
        'width_color': 23
        },
        {
        'bab_quantity_color': 0,
        'comment_color': '',
        'id_color': 3,
        'name_color': '75/23 Золотий',
        'weight_color': 0,
        'width_color': 23}]
    assert response.json == expected_data


@pytest.mark.run(order=100060)
def test_get_one_material(app_fixture):
    client = app_fixture.test_client()
    data = {'id_color': 1}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {
        'bab_quantity_color': 1,
        'bab_weight_color': 150,
        'comment_color': 'дуже білий',
        'id_color': 1,
        'manufacturer_color': 'Ровно',
        'name_color': '77/23 Білий',
        'reserve_color': 0,
        'thickness_color': 36,
        'weight_10m_color': 126,
        'weight_color': 1111,
        'width_color': 23}
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=100070)
def test_chenge_one_material_full(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_change_full': 1,
        'name_color': '77/23 Білий',
        'width_color': 23,
        'bab_quantity_color': 5,
        'weight_color': 5555,
        'comment_color': 'не дуже білий',
        'thickness_color': 36,
        'bab_weight_color': 150,
        'manufacturer_color': 'Ровно',
        'reserve_color': 0,
        'weight_10m_color': 126}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'message': "data_change ok"}
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=100080)
def test_get_one_material_1(app_fixture):
    client = app_fixture.test_client()
    data = {'id_color': 1}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {
        'bab_quantity_color': 5,
        'bab_weight_color': 150,
        'comment_color': 'не дуже білий',
        'id_color': 1,
        'manufacturer_color': 'Ровно',
        'name_color': '77/23 Білий',
        'reserve_color': 0,
        'thickness_color': 36,
        'weight_10m_color': 126,
        'weight_color': 5555,
        'width_color': 23}
    assert response.json == expected_data


@pytest.mark.run(order=100090)
def test_chenge_one_material_weight(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_change': 1,
        'bab_quantity_color': -1,
        'weight_color': -1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'color_change': "ok"}
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=100100)
def test_get_one_material_2(app_fixture):
    client = app_fixture.test_client()
    data = {'id_color': 1}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {
        'bab_quantity_color': 4,
        'bab_weight_color': 150,
        'comment_color': 'не дуже білий',
        'id_color': 1,
        'manufacturer_color': 'Ровно',
        'name_color': '77/23 Білий',
        'reserve_color': 0,
        'thickness_color': 36,
        'weight_10m_color': 126,
        'weight_color': 4444,
        'width_color': 23}
    assert response.json == expected_data
