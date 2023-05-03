import pytest
from flask import json


@pytest.mark.run(order=220010)
def test_read_product_withot_id_product(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/product', headers=headers)
    assert response.status_code == 405
    expected_data = '405 METHOD NOT ALLOWED'
    assert expected_data in str(response)


@pytest.mark.run(order=220020)
def test_read_not_int_id_product(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/product/abc', headers=headers)
    assert response.status_code == 404
    expected_data = '404 NOT FOUND'
    assert expected_data in str(response)


@pytest.mark.run(order=220030)
def test_read_unrial_id_product(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    response = client.get('/product/50')#, headers=headers)
    assert response.status_code == 400
    expected_data = {'id_product': 'ID product 50 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=220032)
def test_put_json_not_correct(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    data = 'this is not valid json'
    response = client.put(
        '/product/1', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'json': 'format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=220034)
def test_post_json_not_correct(app_fixture):
    client = app_fixture.test_client()
    headers = {'Content-Type': 'application/json'}
    data = 'this is not valid json'
    response = client.post(
        '/product', data=data, content_type='application/json')
    assert response.status_code == 400
    expected_data = {'json': 'format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=220040)
def test_edit_unreal_id_product(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-010203",
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 430,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/product/50', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_product': 'ID product 50 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=220050)
def test_create_product_with_repeat_article(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "190-010203",
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'article': 'article 190-010203 already exists'}
    assert response.json == expected_data


@pytest.mark.run(order=220060)
def test_create_product_without_article(app_fixture):
    client = app_fixture.test_client()
    data = {
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/product/2', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'article': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220070)
def test_create_product_with_not_str_article(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": 5,
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий + Червони + Золотий"}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/product/2', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'article': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=220080)
def test_create_product_not_correct_article_123(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": "0-abc01",
    "id_color_1": 1,
    "part_1": 100,
    "id_color_2": None,
    "part_2": None,
    "id_color_3": None,
    "part_3": None,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": "Білий"}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'article': 'is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=220090)
def test_create_product_without_colors(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": ''}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {"colors":  "miss in data"}
    assert response.json == expected_data


@pytest.mark.run(order=220100)
def test_create_product_not_str_colors(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": '',
    "colors": 123}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'colors': 'is not str type'}
    assert response.json == expected_data
    

@pytest.mark.run(order=220105)
def test_create_product_too_short_colors(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": '',
    "colors": '123'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'colors': "can't be less than 5 characters"}
    assert response.json == expected_data


@pytest.mark.run(order=220110)
def test_create_product_without_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'comment':  "miss in data"}
    assert response.json == expected_data


@pytest.mark.run(order=220120)
def test_create_product_not_str_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": [],
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'comment': 'is not str, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=220130)
def test_create_product_without_price(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    # "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'price': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220140)
def test_create_product_not_int_price(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": '400',
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'price': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=220150)
def test_create_product_without_id_color_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    # "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_1': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220160)
def test_create_product_not_int_id_color_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": '1',
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_1': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=220170)
def test_create_product_not_real_id_color_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 10,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_1': f'id_color_1 10 is missing'}
    assert response.json == expected_data



@pytest.mark.run(order=220180)
def test_create_product_without_id_part_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    # "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_1': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220190)
def test_create_product_not_int_id_part_1(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": '33',
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_1': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=220210)
def test_create_product_without_id_color_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    # "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_2': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220220)
def test_create_product_not_int_id_color_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": '2',
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_2': 'is not int, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=220230)
def test_create_product_not_real_id_color_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 10,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_2': f'id_color_2 10 is missing'}
    assert response.json == expected_data



@pytest.mark.run(order=220240)
def test_create_product_without_id_part_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    # "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_2': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220250)
def test_create_product_not_int_id_part_2(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": '33',
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_2': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=220280)
def test_create_product_without_id_color_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    # "id_color_3": 3,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_3': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220290)
def test_create_product_not_int_id_color_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": '3',
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_3': 'is not int, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=220300)
def test_create_product_not_real_id_color_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 10,
    "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_3': f'id_color_3 10 is missing'}
    assert response.json == expected_data



@pytest.mark.run(order=220310)
def test_create_product_without_id_part_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    # "part_3": 33,
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_3': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220320)
def test_create_product_not_int_id_part_3(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": '33',
    "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_3': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=220350)
def test_create_product_without_id_color_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    # "id_color_4": None,
    "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_4': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220360)
def test_create_product_not_int_id_color_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": '1',
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_4': 'is not int, NoneType type'}
    assert response.json == expected_data


@pytest.mark.run(order=220370)
def test_create_product_not_real_id_color_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 1,
    "part_3": 33,
    "id_color_4": 10,
    "part_4": None,
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_color_4': f'id_color_4 10 is missing'}
    assert response.json == expected_data



@pytest.mark.run(order=220380)
def test_create_product_without_id_part_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": 1,
    # "part_4": None,
    "price": 400,
    "comment": 'some',
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_4': 'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=220390)
def test_create_product_not_int_id_part_4(app_fixture):
    client = app_fixture.test_client()
    data = {
    "article": '190-01020',
    "id_color_1": 1,
    "part_1": 33,
    "id_color_2": 2,
    "part_2": 33,
    "id_color_3": 3,
    "part_3": 33,
    "id_color_4": 1,
    "part_4": 'None',
    "price": 400,
    "comment": None,
    "colors": 'Білий + Червони + Золотий'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/product', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'part_4': 'is not int type'}
    assert response.json == expected_data
