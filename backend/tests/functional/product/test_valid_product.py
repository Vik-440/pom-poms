import pytest
from flask import json


@pytest.mark.run(order=200010)
def test_create_product_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-0203",
    "id_color_1": 2,
    "id_part_1": 50,
    "id_color_2": 3,
    "id_part_2": 50,
    "id_color_3": None,
    "id_part_3": None,
    "id_color_4": None,
    "id_part_4": None,
    "price": 380,
    "comment": '',
    "colors": "Червоний + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/create_product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 1}
    assert response.json == expected_data


@pytest.mark.run(order=200020)
def test_create_product_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-0103",
    "id_color_1": 1,
    "id_part_1": 50,
    "id_color_2": 3,
    "id_part_2": 50,
    "id_color_3": None,
    "id_part_3": None,
    "id_color_4": None,
    "id_part_4": None,
    "price": 400,
    "comment": '',
    "colors": "Білий + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/create_product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 2}
    assert response.json == expected_data


@pytest.mark.run(order=200030)
def test_create_product_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-010203",
    "id_color_1": 1,
    "id_part_1": 33,
    "id_color_2": 2,
    "id_part_2": 33,
    "id_color_3": 3,
    "id_part_3": 33,
    "id_color_4": None,
    "id_part_4": None,
    "price": 400,
    "comment": '',
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/create_product', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_product': 3}
    assert response.json == expected_data