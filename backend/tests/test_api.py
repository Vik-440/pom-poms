import json
from app import create_app
from app.api import api



def test_main_route(client):
    with api.app_context():
        # app.config['TESTING'] = True
        # app.config['CONFIG_NAME_PSQL'] = 'testing'

        response = client.get('/finance/methods')
        assert response.status_code == 200

        expected_data = {
            "metod_payment": ["iban", "cash"],
            "outlay_class": [
                    "податок", "мат. осн.", "мат. доп.",
                    "інстр.", "опл. роб.", "реклама", "інше"],
            "filter_class": [
                    "day", "week", "month", "quarter", "year"]
        }

        assert json.loads(response.data) == expected_data
