"""Module payment"""

from flask import jsonify, request
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from app.payments.models import DB_payment
from app.payments.validator import validate_payment
from app import engine
from .. import api
from log.logger import logger
from flasgger import swag_from


@api.route('/finance/payment', methods=['POST'])
@swag_from('/docs/post_payment.yml')
def creating_payment():
    """Create new payment"""
    try:
        data = request.get_json()
    except BadRequest:
        logger.error('/payment(POST) - format json is not correct')
        return jsonify({'payment': 'json format is not correct'}), 400
    error_payment = validate_payment(data)
    if error_payment:
        logger.error(f'{error_payment}')
        return jsonify(error_payment), 400
    try:
        with Session(engine) as session:
            stmt = (
                DB_payment(
                    id_order=data['id_order'],
                    payment=data['payment'],
                    method_payment=data['metod_payment'],
                    data_payment=data['data_payment']))
            session.add(stmt)
            session.commit()
        return jsonify({"message": "creating_payment is excellent"}), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 400
    
