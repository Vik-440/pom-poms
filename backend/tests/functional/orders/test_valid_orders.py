import pytest
from flask import json


@pytest.mark.run(order=700010)
def test_get_main(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main')
    assert response.status_code == 200
    expected_data = [{
        'comment_model': ['some informations'],
        'comment_order': 'test',
        'data_order': '2023-03-03',
        'data_plane_order': '2023-03-23',
        'first_name_client': 'Валина',
        'fulfilled_order': False,
        'id_order': 1,
        'kod_model': ['190-0203'],
        'kolor_model': ['Червоний + Золотий'],
        'np_number': 111,
        'phase_1': [6], 'phase_2': [6], 'phase_3': [3],
        'phone_client': '2222222',
        'phone_recipient': '2222222',
        'quantity_pars_model': [3],
        'real_money': 100,
        'second_name_client': 'Петренко',
        'sity': 'Одеса', 'street_house_apartment': 'вулиця',
        'sum_payment': 1200, 'zip_code': 12345
        }, {
        'comment_model': [None, None, None],
        'comment_order': 'test',
        'data_order': '2023-03-05',
        'data_plane_order': '2023-03-25',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 2,
        'kod_model': ['190-0103', '190-010203', '190-АВС01'],
        'kolor_model': ['Білий + Золотий', 'Білий + Червони + Золотий', 'Білий'],
        'np_number': 111,
        'phase_1': [6, 12, 2], 'phase_2': [6, 12, 2], 'phase_3': [3, 6, 1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [3, 6, 1],
        'real_money': 222,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 4200, 'zip_code': None
        }, {
        'comment_model': [None, None],
        'comment_order': 'test',
        'data_order': '2023-03-07',
        'data_plane_order': '2023-03-27',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 3,
        'kod_model': ['190-03', '190-03023'], 'kolor_model': ['Золотий', 'Золотий'],
        'np_number': 111,
        'phase_1': [22, 44], 'phase_2': [22, 44], 'phase_3': [11, 22],
        'phone_client': '2222222',
        'phone_recipient': '1111111',
        'quantity_pars_model': [11, 22],
        'real_money': 300,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 11440, 'zip_code': None}]
    assert response.json == expected_data


@pytest.mark.run(order=700020)
def test_get_main_date(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?data_start=2023-03-04&data_end=2023-03-06')
    # print(response.json)
    assert response.status_code == 200
    expected_data = [{
        'comment_model': [None, None, None],
        'comment_order': 'test',
        'data_order': '2023-03-05',
        'data_plane_order': '2023-03-25',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 2,
        'kod_model': ['190-0103', '190-010203', '190-АВС01'],
        'kolor_model': ['Білий + Золотий', 'Білий + Червони + Золотий', 'Білий'],
        'np_number': 111,
        'phase_1': [6, 12, 2], 'phase_2': [6, 12, 2], 'phase_3': [3, 6, 1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [3, 6, 1],
        'real_money': 222,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 4200, 'zip_code': None
        }]
    assert response.json == expected_data


@pytest.mark.run(order=700030)
def test_get_main_status(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?fulfilled=true')
    assert response.status_code == 200
    expected_data = [{
        'comment_model': [None],
        'comment_order': 'test',
        'data_order': '2023-03-17',
        'data_plane_order': '2023-03-29',
        'first_name_client': 'Галина',
        'fulfilled_order': True,
        'id_order': 4,
        'kod_model': ['190-АВС01'], 'kolor_model': ['Білий'],
        'np_number': 111,
        'phase_1': [2], 'phase_2': [2], 'phase_3': [1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [1], 'real_money': None,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 11440, 'zip_code': None}]
    assert response.json == expected_data


@pytest.mark.run(order=700040)
def test_get_main_phone(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?phone_client=2222222')
    assert response.status_code == 200
    expected_data = [{
        'comment_model': ['some informations'],
        'comment_order': 'test',
        'data_order': '2023-03-03',
        'data_plane_order': '2023-03-23',
        'first_name_client': 'Валина',
        'fulfilled_order': False,
        'id_order': 1,
        'kod_model': ['190-0203'],
        'kolor_model': ['Червоний + Золотий'],
        'np_number': 111,
        'phase_1': [6], 'phase_2': [6], 'phase_3': [3],
        'phone_client': '2222222',
        'phone_recipient': '2222222',
        'quantity_pars_model': [3],
        'real_money': 100,
        'second_name_client': 'Петренко',
        'sity': 'Одеса', 'street_house_apartment': 'вулиця',
        'sum_payment': 1200, 'zip_code': 12345
        }, {
        'comment_model': [None, None],
        'comment_order': 'test',
        'data_order': '2023-03-07',
        'data_plane_order': '2023-03-27',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 3,
        'kod_model': ['190-03', '190-03023'], 'kolor_model': ['Золотий', 'Золотий'],
        'np_number': 111,
        'phase_1': [22, 44], 'phase_2': [22, 44], 'phase_3': [11, 22],
        'phone_client': '2222222',
        'phone_recipient': '1111111',
        'quantity_pars_model': [11, 22],
        'real_money': 300,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 11440, 'zip_code': None}]
    assert response.json == expected_data


@pytest.mark.run(order=700050)
def test_get_main_id_client(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?id_client=1')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)


@pytest.mark.run(order=700060)
def test_get_main_team(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?team=Місцева-Тутешня')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)

#/main?kolor_like=%D0%B7%D0%BE%D0%BB%D0%BE

@pytest.mark.run(order=700070)
def test_get_main_coach(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?coach=Дивний')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)


@pytest.mark.run(order=700080)
def test_get_main_city(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?city=Київ&fulfilled=all')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 not in str(response.json)
    assert part_data_2 in str(response.json)
    assert part_data_3 not in str(response.json)
    assert part_data_4 in str(response.json)
    # print(response.json)

@pytest.mark.run(order=700090)
def test_get_main_cod_model(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?kod_model=190-0203')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 not in str(response.json)
    assert part_data_4 not in str(response.json)

@pytest.mark.run(order=700100)
def test_get_main_cod_model_like(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?kod_model_like=03023')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 not in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)

@pytest.mark.run(order=700110)
def test_get_main_kolor_like(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?kolor_like=Білий')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 not in str(response.json)
    assert part_data_2 in str(response.json)
    assert part_data_3 not in str(response.json)
    assert part_data_4 not in str(response.json)

@pytest.mark.run(order=700120)
def test_put_main_status_true(app_fixture):
    client = app_fixture.test_client()
    data = {"status_order": True}
    response = client.put('/main/status/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'excellent'}
    assert response.json == expected_data
    response = client.get('/main')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 not in str(response.json)
    assert part_data_2 in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)

@pytest.mark.run(order=700130)
def test_put_main_status_false(app_fixture):
    client = app_fixture.test_client()
    data = {"status_order": False}
    response = client.put('/main/status/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'excellent'}
    assert response.json == expected_data
    response = client.get('/main')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 not in str(response.json)

@pytest.mark.run(order=700140)
def test_put_main_phase(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, 2], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    expected_data = {'message': 'excellent'}
    assert response.json == expected_data
    response = client.get('/main?data_start=2023-03-05&data_end=2023-03-05')
    # print(response.json)
    assert response.status_code == 200
    expected_data = [{
        'comment_model': [None, None, None],
        'comment_order': 'test',
        'data_order': '2023-03-05',
        'data_plane_order': '2023-03-25',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 2,
        'kod_model': ['190-0103', '190-010203', '190-АВС01'],
        'kolor_model': ['Білий + Золотий', 'Білий + Червони + Золотий', 'Білий'],
        'np_number': 111,
        'phase_1': [2, 4, 2], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [3, 6, 1],
        'real_money': 222,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 4200, 'zip_code': None
        }]
    assert response.json == expected_data

@pytest.mark.run(order=700150)
def test_get_main_client_product(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?kod_model=190-010203&id_client=2')
    assert response.status_code == 200
    expected_data = [{
        'comment_model': [None, None, None],
        'comment_order': 'test',
        'data_order': '2023-03-05',
        'data_plane_order': '2023-03-25',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 2,
        'kod_model': ['190-0103', '190-010203', '190-АВС01'],
        'kolor_model': ['Білий + Золотий', 'Білий + Червони + Золотий', 'Білий'],
        'np_number': 111,
        'phase_1': [2, 4, 2], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [3, 6, 1],
        'real_money': 222,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 4200, 'zip_code': None
        }]
    assert response.json == expected_data

@pytest.mark.run(order=700160)
def test_get_main_status_all_without_orders(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?fulfilled=all&phone_client=33333333')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    assert part_data_1 in str(response.json)
    assert part_data_2 in str(response.json)
    assert part_data_3 in str(response.json)
    assert part_data_4 in str(response.json)

@pytest.mark.run(order=700170)
def test_get_main_status_all_without_result(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?data_start=2023-01-05&data_end=2023-01-05')
    assert response.status_code == 200
    part_data_1 = "'id_order': 1"
    part_data_2 = "'id_order': 2"
    part_data_3 = "'id_order': 3"
    part_data_4 = "'id_order': 4"
    # print(response.json)
    assert part_data_1 not in str(response.json)
    assert part_data_2 not in str(response.json)
    assert part_data_3 not in str(response.json)
    assert part_data_4 in str(response.json)

@pytest.mark.run(order=700180)
def test_get_main_client_product_mistake_key(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main?kod_mistake_model=190-010203&id_client=2')
    assert response.status_code == 200
    expected_data = [{
        'comment_model': [None, None, None],
        'comment_order': 'test',
        'data_order': '2023-03-05',
        'data_plane_order': '2023-03-25',
        'first_name_client': 'Галина',
        'fulfilled_order': False,
        'id_order': 2,
        'kod_model': ['190-0103', '190-010203', '190-АВС01'],
        'kolor_model': ['Білий + Золотий', 'Білий + Червони + Золотий', 'Білий'],
        'np_number': 111,
        'phase_1': [2, 4, 2], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1],
        'phone_client': '1111111',
        'phone_recipient': '1111111',
        'quantity_pars_model': [3, 6, 1],
        'real_money': 222,
        'second_name_client': 'Василенко',
        'sity': 'Київ', 'street_house_apartment': None,
        'sum_payment': 4200, 'zip_code': None
        }]
    # print(response.json)
    assert response.json == expected_data