import pytest
from flask import json


@pytest.mark.run(order=820010)
def test_post_statics_not_valid_json(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/finance/payments/statics', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'finance(POST)': 'json format is not correct'}
    assert response.json == expected_data

@pytest.mark.run(order=820020)
def test_post_without_data_key_statics(app_fixture):
    client = app_fixture.test_client()
    data = {'outlay_search': 'anything'}
    response = client.post('/finance/payments/statics', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'statics': 'finance POST error'}
    assert response.json == expected_data


@pytest.mark.run(order=820030)
def test_post_without_date_start_stat(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            # 'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=820040)
def test_post_date_start_stat_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': ['2023-01-01'],
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=820050)
def test_post_date_start_stat_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023+01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_start': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data


@pytest.mark.run(order=820060)
def test_post_without_date_end_stat(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            # 'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=820070)
def test_post_date_end_stat_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': ['2023-04-01'],
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=820080)
def test_post_date_end_stat_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04*01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'data_end': 'is not in format like: yyyy-mm-dd'}
    assert response.json == expected_data

@pytest.mark.run(order=820090)
def test_post_balans_stat_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': ['quarter'],
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'balans': 'is not str type'}
    assert response.json == expected_data

@pytest.mark.run(order=820100)
def test_post_balance_not_valid(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'nothing',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'balans': 'key is not valid'}
    assert response.json == expected_data

@pytest.mark.run(order=820110)
def test_post_without_iban_stat(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            # 'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'iban': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=820120)
def test_post_date_iban_not_bool(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': 'True',
            'cash': False}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'iban': 'is not bool type'}
    assert response.json == expected_data

@pytest.mark.run(order=820130)
def test_post_without_cash_stat(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            # 'cash': False
            }
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'cash': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=820140)
def test_post_date_cash_not_bool(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': 'False'}
    response = client.post(
        '/finance/payments/statics',
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'cash': 'is not bool type'}
    assert response.json == expected_data