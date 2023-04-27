import pytest
from flask import json


@pytest.mark.run(order=120010)
def test_post_json_not_correct_materials(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.post('/materials', data=data)
    assert response.status_code == 400
    expected_data = {'materials': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=120020)
def test_materials_without_comment(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'comment':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120030)
def test_materials_comment_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': ['дуже білий'],
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'comment': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=120040)
def test_materials_without_manufacturer(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        # 'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'manufacturer':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120050)
def test_materials_manufacturer_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': ['Ровно'],
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'manufacturer': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=120060)
def test_materials_without_name(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        # 'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'name':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120070)
def test_materials_name_not_str(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': ('77/23 Білий',),
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'name': 'is not str type'}
    assert response.json == expected_data


@pytest.mark.run(order=120080)
def test_materials_without_reserve(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        # 'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'reserve':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120090)
def test_materials_reserve_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': '0',
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'reserve': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120100)
def test_materials_without_spool_qty(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        # 'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'spool_qty':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120110)
def test_materials_spool_qty_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': [1],
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'spool_qty': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120120)
def test_materials_without_spool_weight(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        # 'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'spool_weight':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120130)
def test_materials_spool_weight_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': '150',
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'spool_weight': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120140)
def test_materials_without_thickness(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        # 'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'thickness':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120150)
def test_materials_thickness_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': [36],
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'thickness': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120160)
def test_materials_without_width(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        # 'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'width':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120170)
def test_materials_width_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': [23],
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'width': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120180)
def test_materials_without_weight_10m(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        # 'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'weight_10m':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120190)
def test_materials_weight_10m_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': '12.623',
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'weight_10m': 'is not int or float type'}
    assert response.json == expected_data


@pytest.mark.run(order=120200)
def test_materials_without_weight(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        # 'weight': 1111
        }
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'weight':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120210)
def test_materials_weight_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': [1111]}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'weight': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120220)
def test_materials_new_name_already_exits(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/materials', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'name': f'name 77/23 Білий already exists'}
    assert response.json == expected_data


@pytest.mark.run(order=120230)
def test_materials_get_args_unreal(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials?available=misstake')
    assert response.status_code == 400
    expected_data = {'materials': 'misstake in args'}
    assert response.json == expected_data


@pytest.mark.run(order=120240)
def test_materials_get_unreal_id(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/materials/111')
    assert response.status_code == 400
    expected_data = {'id_material': f'ID product 111 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=120250)
def test_put_json_not_correct_materials(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/materials/1', data=data)
    assert response.status_code == 400
    expected_data = {'materials': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=120260)
def test_put_json_not_correct_materials_consumption(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/materials/consumption/1', data=data)
    assert response.status_code == 400
    expected_data = {'materials': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=120270)
def test_materials_consumption_without_edit_spool_qty(app_fixture):
    client = app_fixture.test_client()
    data = {
        # 'edit_spool_qty': -1,
        'edit_weight': -1111
        }
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'edit_spool_qty':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120280)
def test_materials_consumption_edit_spool_qty_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'edit_spool_qty': '-1',
        'edit_weight': -1111
        }
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'edit_spool_qty': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120290)
def test_materials_consumption_without_edit_weight(app_fixture):
    client = app_fixture.test_client()
    data = {
        'edit_spool_qty': -1,
        # 'edit_weight': -1111
        }
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'edit_weight':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=120300)
def test_materials_consumption_edit_weight_not_int(app_fixture):
    client = app_fixture.test_client()
    data = {
        'edit_spool_qty': -1,
        'edit_weight': [-1111]
        }
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'edit_weight': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120310)
def test_materials_weight_not_int_put(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': [1111]}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'weight': 'is not int type'}
    assert response.json == expected_data


@pytest.mark.run(order=120320)
def test_materials_not_real_id_material_put(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/111', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_material': f'ID product 111 is invalid'}
    assert response.json == expected_data


@pytest.mark.run(order=120330)
def test_materials_new_name_already_exits_put(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '75/23 Золотий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/1', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'name': f'name 75/23 Золотий already exists'}
    assert response.json == expected_data


@pytest.mark.run(order=120340)
def test_materials_not_real_id_material_put_consumption(app_fixture):
    client = app_fixture.test_client()
    data = {
        'comment': 'дуже білий',
        'manufacturer': 'Ровно',
        'name': '77/23 Білий',
        'reserve': 0,
        'spool_qty': 1,
        'spool_weight': 150,
        'thickness': 36,
        'width': 23,
        'weight_10m': 12.623,
        'weight': 1111}
    headers = {'Content-Type': 'application/json'}
    response = client.put('/materials/consumption/111', data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    expected_data = {'id_material': f'ID product 111 is invalid'}
    assert response.json == expected_data