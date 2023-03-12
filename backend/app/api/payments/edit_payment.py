"""module rof changing data in payment"""

from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/payment/<int:id_payment>', methods=['PUT'])
def payment_changing(id_payment):
    """module rof changing data in payment"""
    try:
        data = request.get_json()
        print(data)
        with Session(engine)as session:
            stmt = (
                update(DB_payment)
                .where(DB_payment.id_payment == id_payment)
                .values(
                    payment=data['payment'],
                    method_payment=data['metod_payment'],
                    data_payment=data['data_payment']))
            session.execute(stmt)
            session.commit()
        return jsonify({"message": "payment_changing excellent"}), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500
    