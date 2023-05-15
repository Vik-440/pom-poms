import pytest


@pytest.mark.run(order=910010)
def test_autofill_phone(app_fixture):
    client = app_fixture.test_client()
    params = {'abcde': '111'}
    expected_data = {'autofill': 'request does not have searching keys'}
    response = client.get('/autofill', query_string=params)
    assert response.status_code == 200
    assert response.json == expected_data