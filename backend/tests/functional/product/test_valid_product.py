import pytest
from flask import json


@pytest.mark.run(order=200010)
def test_create_product_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-0203",
    "id_color_1": 2,
    "part_1": 50,
    "id_color_2": 3,
    "part_2": 50,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 380,
    "comment": 'some informations',
    "colors": "Червоний + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 1}
    assert response.json == expected_data


@pytest.mark.run(order=200020)
def test_create_product_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-0103",
    "id_color_1": 1,
    "part_1": 50,
    "id_color_2": 3,
    "part_2": 50,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 2}
    assert response.json == expected_data


@pytest.mark.run(order=200030)
def test_create_product_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-010203",
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 3}
    assert response.json == expected_data


@pytest.mark.run(order=200040)
def test_read_product_1(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/product/3', headers=headers)
    assert response.status_code == 200
    expected_data = {
        'id_product': 3,
        'article': '190-010203',
        'colors': 'Білий + Червони + Золотий',
        'comment': None,
        'id_color_1': 1,
        'id_color_2': 2,
        'id_color_3': 3,
        'id_color_4': None,
        'part_1': 33,
        'part_2': 33,
        'part_3': 33,
        'part_4': None,
        'color_name_1': '77/23 Білий',
        'color_name_2': '70/23 Червоний',
        'color_name_3': '75/23 Золотий',
        'color_name_4': None,
        'price': 400}
    assert response.json == expected_data


@pytest.mark.run(order=200050)
def test_edit_product(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-010203",
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 430,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/product/3', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'edit_product': 3}
    assert response.json == expected_data

    response = client.get('/product/3', headers=headers)
    assert response.status_code == 200
    expected_data = {
        'id_product': 3,
        'article': '190-010203',
        'colors': 'Білий + Червони + Золотий',
        'comment': None,
        'id_color_1': 1,
        'id_color_2': 2,
        'id_color_3': 3,
        'id_color_4': None,
        'part_1': 33,
        'part_2': 33,
        'part_3': 33,
        'part_4': None,
        'color_name_1': '77/23 Білий',
        'color_name_2': '70/23 Червоний',
        'color_name_3': '75/23 Золотий',
        'color_name_4': None,
        'price': 430}
    assert response.json == expected_data


@pytest.mark.run(order=200060)
def test_create_product_not_correct_article(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-abc01",
    "id_color_1": 1,
    "part_1": 100,
    "id_color_2": None,
    "part_2": None,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 4}
    assert response.json == expected_data

    response = client.get('/product/4', headers=headers)
    assert response.status_code == 200
    expected_data = {
        'id_product': 4,
        'article': '190-АВС01',
        'colors': 'Білий',
        'comment': None,
        'id_color_1': 1,
        'id_color_2': None,
        'id_color_3': None,
        'id_color_4': None,
        'part_1': 100,
        'part_2': None,
        'part_3': None,
        'part_4': None,
        'color_name_1': '77/23 Білий',
        'color_name_2': None,
        'color_name_3': None,
        'color_name_4': None,
        'price': 400}
    assert response.json == expected_data


@pytest.mark.run(order=200070)
def test_create_product_not_real_procent_part_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03',
    "id_color_1": 3,
    "part_1": 333,
    "id_color_2": None,
    "part_2": None,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 5}
    assert response.json == expected_data

    response = client.get('/product/5', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 5,
    "article": '190-03',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": None,
    "part_2": None,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    'color_name_1': '75/23 Золотий',
    'color_name_2': None,
    'color_name_3': None,
    'color_name_4': None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data
 

@pytest.mark.run(order=200080)
def test_create_product_not_real_procent_id_part_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03020',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 222,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 6}
    assert response.json == expected_data

    response = client.get('/product/6', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 6,
    "article": '190-03020',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    'color_name_1': '75/23 Золотий',
    'color_name_2': '70/23 Червоний',
    'color_name_3': None,
    'color_name_4': None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data



@pytest.mark.run(order=200090)
def test_create_product_only_1_mateial(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03021',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": None,
    "part_2": 222,
    "id_color_3": 222,
    "part_3": 222,
    "id_color_4": 222,
    "part_4": 222,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 7}
    assert response.json == expected_data

    response = client.get('/product/7', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 7,
    "article": '190-03021',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": None,
    "part_2": None,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data



@pytest.mark.run(order=200100)
def test_create_product_not_real_procent_id_part_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03022',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 111,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 8}
    assert response.json == expected_data

    response = client.get('/product/8', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 8,
    "article": '190-03022',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 100,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data


@pytest.mark.run(order=200110)
def test_create_product_only_2_mateials(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03023',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": None,
    "part_3": 222,
    "id_color_4": 222,
    "part_4": 222,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 9}
    assert response.json == expected_data

    response = client.get('/product/9', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 9,
    "article": '190-03023',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data



@pytest.mark.run(order=200120)
def test_create_product_not_real_procent_id_part_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03024',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 100,
    "id_color_4": 1,
    "part_4": 444,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 10}
    assert response.json == expected_data

    response = client.get('/product/10', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 10,
    "article": '190-03024',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 100,
    "id_color_4": 1,
    "part_4": 100,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data



@pytest.mark.run(order=200130)
def test_create_product_only_3_mateials(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-03025',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 100,
    "id_color_4": None,
    "part_4": 222,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 11}
    assert response.json == expected_data

    response = client.get('/product/11', headers=headers)
    assert response.status_code == 200
    expected_data = {
    'id_product': 11,
    "article": '190-03025',
    "id_color_1": 3,
    "part_1": 100,
    "id_color_2": 2,
    "part_2": 100,
    "id_color_3": 1,
    "part_3": 100,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Золотий'}
    assert response.json == expected_data

