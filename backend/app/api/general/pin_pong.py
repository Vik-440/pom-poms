"""Ping Pong - testing connections with app"""

from flask import jsonify
from .. import api
from flasgger import swag_from


@api.route('/ping', methods=['GET'])
# @swag_from('/docs/get_autofill_product_client_material.yml')
def ping_pong():
    """Ping Pong - testing connections with app"""
    return jsonify({'ping': 'pong'}), 200