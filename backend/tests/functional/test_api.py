# from app import create_app
import pytest


@pytest.mark.run(order=300030)
def test_attributes_payments(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/finance/methods')
    assert response.status_code == 200
    expected_data = {
                "metod_payment": ["iban", "cash"],
                "outlay_class": [
                        "податок", "мат. осн.", "мат. доп.",
                        "інстр.", "опл. роб.", "реклама", "інше"],
                "filter_class": [
                        "day", "week", "month", "quarter", "year"]}
    assert response.json == expected_data


# @pytest.mark.run(order=20)
# def test_get_main(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/main')
#     print(response.json)
#     assert response.status_code == 200


# @pytest.mark.run(order=30)
# def test_get_order(app_fixture):
#     client = app_fixture.test_client()
#     response = client.get('/read_order/11')
#     print(response.json)
#     assert response.status_code == 200


# pytest.exit("Test is not allowed to run with a real database")
# session.execute(DB_client.__table__.delete())
# session.commit()
