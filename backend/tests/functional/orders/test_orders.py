import pytest


@pytest.mark.run(order=800010)
def test_get_main(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main')
    # print(response.json)
    assert response.status_code == 200