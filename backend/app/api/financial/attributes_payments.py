"""Module creating rules for finance page"""

from flask import jsonify
from .. import api


@api.route('/finance/methods', methods=['GET'])
def attributes_payments():
    full_block = {
        "metod_payment": ["iban", "cash"],
        "outlay_class": [
                "податок", "мат. осн.", "мат. доп.",
                "інстр.", "опл. роб.", "реклама", "інше", "офіс"],
        "filter_class": [
                "day", "week", "month", "quarter", "year"]}
    return jsonify(full_block), 200
