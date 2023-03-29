# from app import create_app


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


def test_get_main(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/main')
    print(response.json)
    assert response.status_code == 200


def test_get_order(app_fixture):
    client = app_fixture.test_client()
    response = client.get('/read_order/11')
    print(response.json)
    assert response.status_code == 200


# session.execute(DB_client.__table__.delete())
# session.commit()