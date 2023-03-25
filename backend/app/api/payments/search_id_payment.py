"""Search payments by id order"""

from datetime import datetime
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/order_payments', methods=['POST'])
def payment_id_order_searching():
    """Search payments by id order"""
    try:
        data = request.get_json()
        if 'id_order' in data:
            with Session(engine)as session:
                id_order = data['id_order']
                select_block = select(
                    DB_payment.id_payment,
                    DB_payment.id_order,
                    DB_payment.payment,
                    DB_payment.method_payment,
                    DB_payment.data_payment)
                stmt = (
                    select_block
                    .where(DB_payment.id_order == id_order)
                    .order_by(DB_payment.data_payment))
                payments = session.execute(stmt).all()
                full_block = []
                for row in payments:
                    one_block = {"id_payment": row.id_payment,
                                "id_order": row.id_order,
                                "payment": row.payment,
                                "metod_payment": row.method_payment,
                                "data_payment": str(row.data_payment)}
                    full_block.append(one_block)
            return jsonify(full_block)
    except Exception as e:
        logger.error(f'Error in finance_payments_order POST: {e}')
        return f'Error in order_payments POST: {e}', 400
    