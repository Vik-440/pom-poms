import pytest
from flask import json


@pytest.mark.run(order=120010)
def test_create_material_3(app_fixture):
    client = app_fixture.test_client()
    data = {
        'color_new_misstake': 0,
        'name_color': '75/23 Золотий',
        'width_color': 23,
        'bab_quantity_color': 0,
        'weight_color': 0,
        'comment_color': '',
        'thickness_color': 36,
        'bab_weight_color': 160,
        'manufacturer_color': 'Ровно',
        'reserve_color': 0,
        'weight_10m_color': 128}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/material', data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    expected_data = {'message': 'request is not correct'}
    assert response.json == expected_data