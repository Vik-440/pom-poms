import pytest
from flask import json


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