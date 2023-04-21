import pytest
from flask import json


@pytest.mark.run(order=720005)
def test_read_unrial_id_order_put_status(app_fixture):
    client = app_fixture.test_client()
    data = {'status_order': False}
    response = client.put('/main/status/10', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 10 is not exist'}
    assert response.json == expected_data



@pytest.mark.run(order=720010)
def test_put_json_not_correct_status(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/main/status/1', data=data)
    assert response.status_code == 400
    expected_data = {'status(PUT)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=720020)
def test_order_without_status_order(app_fixture):
    client = app_fixture.test_client()
    data = {'status_order_1': False}
    response = client.put('/main/status/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'status_order':  'miss in data'}
    assert response.json == expected_data


@pytest.mark.run(order=720030)
def test_order_not_correct_status_order(app_fixture):
    client = app_fixture.test_client()
    data = {'status_order': 'False'}
    response = client.put('/main/status/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'status_order': 'is not bool type'}
    assert response.json == expected_data


@pytest.mark.run(order=720040)
def test_put_json_not_correct_phase(app_fixture):
    client = app_fixture.test_client()
    data = 'this is not valid json'
    response = client.put('/main/phase/1', data=data)
    assert response.status_code == 400
    expected_data = {'phases(PUT)': 'json format is not correct'}
    assert response.json == expected_data


@pytest.mark.run(order=720050)
def test_read_unrial_id_order_put_phase(app_fixture):
    client = app_fixture.test_client()
    data = {'status_order': False}
    response = client.put('/main/phase/10', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'id_order': 'ID order 10 is not exist'}
    assert response.json == expected_data

@pytest.mark.run(order=720060)
def test_put_main_phase_mistake(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_1': 'misstake in qty phases in data'}
    assert response.json == expected_data

@pytest.mark.run(order=720070)
def test_put_main_phase_str(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, '5'], 'phase_2': [2, 4, 2], 'phase_3': [2, 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_1': 'has data not int type'}
    assert response.json == expected_data

@pytest.mark.run(order=720080)
def test_put_main_phase_mistake_2(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, 1], 'phase_2': [2, 4], 'phase_3': [2, 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_2': 'misstake in qty phases in data'}
    assert response.json == expected_data

@pytest.mark.run(order=720090)
def test_put_main_phase_str_2(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, 5], 'phase_2': [2, 4, '2'], 'phase_3': [2, 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_2': 'has data not int type'}
    assert response.json == expected_data

@pytest.mark.run(order=720100)
def test_put_main_phase_mistake_3(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, 2], 'phase_2': [2, 4, 2], 'phase_3': [2, 4]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_3': 'misstake in qty phases in data'}
    assert response.json == expected_data

@pytest.mark.run(order=720110)
def test_put_main_phase_str_3(app_fixture):
    client = app_fixture.test_client()
    data = {'phase_1': [2, 4, 5], 'phase_2': [2, 4, 2], 'phase_3': ['2', 4, 1]}
    response = client.put('/main/phase/2', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    expected_data = {'phase_3': 'has data not int type'}
    assert response.json == expected_data
