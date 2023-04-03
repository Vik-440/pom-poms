import pytest


@pytest.mark.run(order=10)
def test_connect_testing(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/ping')
    if response.status_code != 200:
        pytest.exit("Test is not allowed to run with a real database")
    assert response.status_code == 200
    expected_data = {'ping': 'pong'}
    assert response.json == expected_data
