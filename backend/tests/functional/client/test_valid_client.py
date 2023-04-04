import pytest
from flask import json


@pytest.mark.run(order=300010)
def test_create_client_with_normalize_data(app_fixture):
    client = app_fixture.test_client()
    data = {
        'phone': '1111111',
        'second_name': 'Василенко',
        'first_name': 'Галина',
        'surname': None,
        'city': 'Київ',
        'np_number': 111,
        'team': None,
        'coach': "ма'Рга-тир бур",
        'zip_code': None,
        'address': None,
        'comment': None}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/client', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_client': 1}
    assert response.json == expected_data


@pytest.mark.run(order=300020)
def test_read_client_1(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/client/1', headers=headers)
    expected_data = {
        'id_client': 1,
        'phone': '1111111',
        'second_name': 'Василенко',
        'first_name': 'Галина',
        'surname': None,
        'city': 'Київ',
        'np_number': 111,
        'team': None,
        'coach': "Ма'рга-Тир Бур",
        'zip_code': None,
        'address': None,
        'comment': None}
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=300030)
def test_edit_client(app_fixture):
    client = app_fixture.test_client()
    data = {
        'phone': '+22-22 22a2',
        'second_name': 'петренко',
        'first_name': 'валина',
        'surname': "кру'Мпа",
        'city': 'одеса',
        'np_number': 111,
        'team': 'місцева-тутешня',
        'coach': 'дивниЙ',
        'zip_code': 12345,
        'address': 'вулиця',
        'comment': 'тестування'}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/client/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'edit_client': 1}
    assert response.json == expected_data


@pytest.mark.run(order=300040)
def test_read_client_1(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/client/1', headers=headers)
    expected_data = {
        'id_client': 1,
        'phone': '2222222',
        'second_name': 'Петренко',
        'first_name': 'Валина',
        'surname': "Кру'мпа",
        'city': 'Одеса',
        'np_number': 111,
        'team': 'Місцева-Тутешня',
        'coach': 'Дивний',
        'zip_code': 12345,
        'address': 'вулиця',
        'comment': 'тестування'}
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=300050)
def test_create_client_2(app_fixture):
    client = app_fixture.test_client()
    data = {
        'phone': '1111111',
        'second_name': 'Василенко',
        'first_name': 'Галина',
        'surname': None,
        'city': 'Київ',
        'np_number': 111,
        'team': None,
        'coach': "ма'Рга-тир бур",
        'zip_code': None,
        'address': None,
        'comment': None}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/client', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'id_client': 2}
    assert response.json == expected_data
