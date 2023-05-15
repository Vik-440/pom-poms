import pytest


@pytest.mark.run(order=900010)
def test_autofill_empty(app_fixture):
    client = app_fixture.test_client()
    expected_data = {'args': ['phone', 'second_name', 'city', 'team',
                              'coach', 'article', 'name_material']}
    response = client.get('/autofill')
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900020)
def test_autofill_phone(app_fixture):
    client = app_fixture.test_client()
    params = {'phone': '111'}
    expected_data = [{'id_client': 2, 'value': '1111111'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data
    # print(response.json)


@pytest.mark.run(order=900030)
def test_autofill_second_name(app_fixture):
    client = app_fixture.test_client()
    params = {'second_name': 'пет'}
    expected_data = [{'id_client': 1, 'value': 'Петренко Валина'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900040)
def test_autofill_city(app_fixture):
    client = app_fixture.test_client()
    params = {'city': 'дес'}
    expected_data = [{'value': 'Одеса'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900050)
def test_autofill_team(app_fixture):
    client = app_fixture.test_client()
    params = {'team': 'тут'}
    expected_data = [{'value': 'Місцева-Тутешня'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900060)
def test_autofill_coach(app_fixture):
    client = app_fixture.test_client()
    params = {'coach': 'ний'}
    expected_data = [{'value': 'Дивний'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900070)
def test_autofill_article(app_fixture):
    client = app_fixture.test_client()
    params = {'article': '190-a'}
    expected_data = [{
                'id_product': 4,
                'value': '190-АВС01'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data


@pytest.mark.run(order=900080)
def test_autofill_name_material(app_fixture):
    client = app_fixture.test_client()
    params = {'name_material': 'олот'}
    expected_data = [{
                'id_material': 3,
                'value': '75/23 Золотий'}]
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data
