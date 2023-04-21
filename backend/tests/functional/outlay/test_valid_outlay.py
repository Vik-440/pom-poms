import pytest
from flask import json
from datetime import datetime
# from unittest.mock import MagicMock, patch, PropertyMock
from unittest.mock import patch
from freezegun import freeze_time



@pytest.mark.run(order=600010)
def test_create_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_outlay': 1,
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 100,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'creating_outlay is excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=600020)
def test_edit_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_outlay': 1,
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}
    response = client.put('/finance/outlay/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'outlay_changing excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=600030)
def test_read_outlay(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/finance/outlays')
    assert response.status_code == 200
    expected_data = [{
        'id_outlay': 1,
        'data_outlay': '2023-03-03',
        'id_outlay_class': 'податок',
        'money_outlay': 125,
        'comment_outlay': 'ПриватБанк'}]
    assert response.json == expected_data


@pytest.mark.run(order=600040)
def test_create_outlay_1(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'id_outlay': 1,
        'data_outlay': '2023-03-05',
        'id_outlay_class': 'податок',
        'money_outlay': 200,
        'comment_outlay': 'ПриватБанк'}
    response = client.post('/finance/outlay', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'creating_outlay is excellent'}
    assert response.json == expected_data


@pytest.mark.run(order=600050)
def test_search_outlay(app_fixture):
    client = app_fixture.test_client()
    data = {
        'outlay_search': 'anything',
        'data_start': '2023-03-01',
        'data_end': '2023-03-04'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [{
        'comment_outlay': 'ПриватБанк',
        'data_outlay': '2023-03-03',
        'id_outlay': 1,
        'id_outlay_class': 'податок',
        'money_outlay': 125}]
    assert response.json == expected_data


@freeze_time('2023-04-21')
@pytest.mark.run(order=600060)
def test_finance_statistic(app_fixture):
    client = app_fixture.test_client()
    data = {'stat': 'anything'}
    response = client.post('/finance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {
        'stat_outlay': [1078, 325, 325, None, None, None, None],
        'stat_payment': [2064, 622, 622, None, None, None, None]}
    # print(response.json)
    assert response.json == expected_data