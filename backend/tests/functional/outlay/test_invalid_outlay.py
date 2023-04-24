import pytest
from flask import json


@pytest.mark.run(order=620010)
def test_post_outlay_not_valid_json(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance/outlay', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'outlay(POST)': 'json format is not correct'}
    assert response.json == expected_data



@pytest.mark.run(order=620020)
def test_post_without_date_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_outlay': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620030)
def test_post_data_date_outlay_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': ['2023-03-03'],
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_outlay': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620040)
def test_post_date_outlay_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023.03.03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_outlay': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=620050)
def test_post_without_id_outlay_class(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        # 'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_outlay_class': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620060)
def test_post_id_outlay_class_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': ['податок'],
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_outlay_class': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620070)
def test_post_id_outlay_class_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'test',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_outlay_class': 'is not valid'}
    assert response.json == expected_data


@pytest.mark.run(order=620080)
def test_post_without_money_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        # 'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'money_outlay': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620090)
def test_post_money_outlay_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': '125',
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'money_outlay': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=620100)
def test_post_without_comment_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        # 'comment_outlay': 'ПриватБанк'
        }
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'comment_outlay': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620110)
def test_post_comment_outlay_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': ['ПриватБанк']}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'comment_outlay': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620120)
def test_put_outlay_not_valid_json(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/finance/outlay/1', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'outlay(PUT)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=620110)
def test_put_comment_outlay_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': ['ПриватБанк']}
    response = client.put('/finance/outlay/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'comment_outlay': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620120)
def test_post_outlay_not_valid_json_1(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'finance(POST)': 'json format is not correct'}
    assert response.json == expected_data

@pytest.mark.run(order=620130)
def test_post_without_data(app_fixture):
    client = app_fixture.test_client()
    data = {'json': 'empty'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'message': 'finance POST error'}
    assert response.json == expected_data


@pytest.mark.run(order=620140)
def test_post_without_date_search_start_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'data_start': '2023-03-03',
        'data_end': '2023-03-03',
         'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620150)
def test_post_date_start_search_outlay_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': ['2023-03-03'],
        'data_end': '2023-03-03',
         'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620160)
def test_post_date_start_search_outlay_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023+03-.03',
        'data_end': '2023-03-03',
         'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data

@pytest.mark.run(order=620170)
def test_post_without_date_search_end_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-03',
        # 'data_end': '2023-03-03',
        'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=620180)
def test_post_date_end_search_outlay_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-03',
        'data_end': ['2023-03-03'],
         'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=620190)
def test_post_date_end_search_outlay_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {
        'data_start': '2023-03-03',
        'data_end': '2023=03+03',
         'outlay_search': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data