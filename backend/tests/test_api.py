import json
from app import create_app
import pytest
from flask import Flask

def test_attributes_payments(client):
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
