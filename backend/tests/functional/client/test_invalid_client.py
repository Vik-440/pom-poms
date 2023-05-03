import pytest
from flask import json


@pytest.mark.run(order=320010)
def test_read_client_withot_id_product(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/client', headers=headers)
    assert response.status_code == 405
    expected_data = '405 METHOD NOT ALLOWED'
    assert expected_data in str(response)


@pytest.mark.run(order=320020)
def test_read_not_int_id_client(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/client/abc', headers=headers)
    assert response.status_code == 404
    expected_data = '404 NOT FOUND'
    assert expected_data in str(response)


@pytest.mark.run(order=320030)
def test_read_unrial_id_client_get(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/client/5', headers=headers)
    assert response.status_code == 400
    expected_data = {'id_client': 'ID client 5 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=320040)
def test_read_unrial_id_client_put(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    data = {'test': 'test'}
    response = client.put('/client/5', data=data, headers=headers)
    assert response.status_code == 400
    expected_data = {'id_client': 'ID client 5 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=320050)
def test_post_json_not_correct(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    data = 'this is not valid json'
    response = client.post(
        '/client', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'json': 'format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=320060)
def test_put_json_not_correct(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    data = 'this is not valid json'
    response = client.put(
        '/client/1', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'json': 'format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=320070)
def test_create_client_number_is_into_DB(app_fixture):
    client = app_fixture.test_client()
    data = {
        'phone': '2222222',
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
    response = client.post('/client', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'phone': 'mobile number 2222222 already exists'}
    assert response.json == expected_data


@pytest.mark.run(order=320080)
def test_client_without_address(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'address':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320090)
def test_client_not_str_address(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': ['вулиця'],
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'address': 'is not str, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=320100)
def test_client_without_city(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        # 'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'city':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320110)
def test_client_not_str_city(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': ('одеса',),
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'city': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=320120)
def test_client_without_coach(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        # 'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'coach':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320130)
def test_client_not_str_coach(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 111,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'coach': 'is not str, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=320140)
def test_client_without_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        # 'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'comment':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320150)
def test_client_not_str_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': ['тестування'],
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'comment': 'is not str, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=320160)
def test_client_without_first_name(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        # 'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'first_name':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320170)
def test_client_not_str_first_name(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': ['валина'],
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'first_name': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=320180)
def test_client_without_second_name(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        # 'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'second_name':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320190)
def test_client_not_str_second_name(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': ('петренко',),
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'second_name': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=320200)
def test_client_without_surname(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        # 'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'surname':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320210)
def test_client_not_str_surname(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': ["кру'Мпа"],
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'surname': 'is not str, NoneType type'}
    assert response.json == expected_data



@pytest.mark.run(order=320220)
def test_client_without_team(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        # 'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'team':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320230)
def test_client_not_str_team(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 11111111,
        'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'team': 'is not str, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=320240)
def test_client_without_np_number(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        # 'np_number': 111,
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'np_number':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320250)
def test_client_not_str_np_number(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': None,
        'np_number': '111',
        'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'np_number': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=320260)
def test_client_without_phone(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        # 'phone': '2222222',
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phone':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320270)
def test_client_not_str_phone(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': None,
        'np_number': 111,
        'phone': [22222223],
        'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phone': 'is not str, int type'}
    assert response.json == expected_data


@pytest.mark.run(order=320280)
def test_client_without_zip_code(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': 'дивниЙ',
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': 'місцева-тутешня',
        'np_number': 111,
        'phone': '2222222'}
        # 'zip_code': 12345}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'zip_code':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=320290)
def test_client_not_str_zip_code(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': None,
        'np_number': 111,
        'phone': '22222223',
        'zip_code': '12345'}
    response = client.post('/client', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'zip_code': 'is not int, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=320300)
def test_client_not_str_zip_code_put(app_fixture):
    client = app_fixture.test_client()
    data = {
        'address': 'вулиця',
        'city': 'одеса',
        'coach': None,
        'comment': 'тестування',
        'first_name': 'валина',
        'second_name': 'петренко',
        'surname': "кру'Мпа",
        'team': None,
        'np_number': 111,
        'phone': '22222223',
        'zip_code': '12345'}
    response = client.put('/client/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'zip_code': 'is not int, NoneType type'}
    assert response.json == expected_data