from freezegun import freeze_time
import pytest
from flask import json


@pytest.mark.run(order=800010)
def test_attributes_payments(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/finance/methods')
    assert response.status_code == 200
    expected_data = {
                "metod_payment": ["iban", "cash"],
                "outlay_class": [
                        "податок", "мат. осн.", "мат. доп.",
                        "інстр.", "опл. роб.", "реклама", "інше", 'офіс'],
                "filter_class": [
                        "day", "week", "month", "quarter", "year"]}
    assert response.json == expected_data


@freeze_time('2023-04-21')
@pytest.mark.run(order=800020)
def test_finance_payment_statistic_day(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'day',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': True}
    response = client.post(
        '/finance/payments/statics', 
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [
        {'data_payment': '2023-03-03', 'metod_payment': 'all', 'payment': 100, 'payment_quantity': 1},
        {'data_payment': '2023-03-05', 'metod_payment': 'all', 'payment': 222, 'payment_quantity': 1},
        {'data_payment': '2023-03-07', 'metod_payment': 'all', 'payment': 300, 'payment_quantity': 1}]
    assert response.json == expected_data


@freeze_time('2023-04-21')
@pytest.mark.run(order=800030)
def test_finance_payment_statistic_week(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'week',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': True}
    response = client.post(
        '/finance/payments/statics', 
        data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = [
        {'data_payment': '2023-02-26', 'metod_payment': 'all', 'payment': 100, 'payment_quantity': 1},
        {'data_payment': '2023-03-05', 'metod_payment': 'all', 'payment': 522, 'payment_quantity': 2}]
    assert response.json == expected_data

@freeze_time('2023-04-21')
@pytest.mark.run(order=800040)
def test_finance_payment_statistic_month(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'month',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': False,
            'cash': True}
    response = client.post(
        '/finance/payments/statics', 
        data=json.dumps(data), content_type='application/json')
#     print(response.json)
    assert response.status_code == 200
    expected_data = [
        {'data_payment': '2023-03-03', 'metod_payment': 'cash', 'payment': 222, 'payment_quantity': 1}]
    assert response.json == expected_data


@freeze_time('2023-04-21')
@pytest.mark.run(order=800050)
def test_finance_payment_statistic_quarter(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'quarter',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': True,
            'cash': False}
    response = client.post(
        '/finance/payments/statics', 
        data=json.dumps(data), content_type='application/json')
#     print(response.json)
    assert response.status_code == 200
    expected_data = [
        {'data_payment': '2023-01-01', 'metod_payment': 'iban', 'payment': 400, 'payment_quantity': 2}]
    assert response.json == expected_data

@freeze_time('2023-04-21')
@pytest.mark.run(order=800060)
def test_finance_payment_statistic_year(app_fixture):
    client = app_fixture.test_client()
    data = {'balans': 'year',
            'data_start': '2023-01-01',
            'data_end': '2023-04-01',
            'iban': False,
            'cash': False}
    response = client.post(
        '/finance/payments/statics', 
        data=json.dumps(data), content_type='application/json')
#     print(response.json)
    assert response.status_code == 200
    expected_data = [
        {'data_payment': '2023-01-01', 'metod_payment': 'all', 'payment': 622, 'payment_quantity': 3}]
    assert response.json == expected_data