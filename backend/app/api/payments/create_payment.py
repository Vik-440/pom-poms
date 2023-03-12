"""Module for create payment"""

from flask import jsonify, request
# from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.payments.models import DB_payment
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/payment', methods=['POST'])
def creating_payment():
    try:
        data = request.get_json()
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
        return f'Error in function finance: {e}', 500
    