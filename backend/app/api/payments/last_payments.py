"""Module for extract last payments for finance page"""

from datetime import datetime
from flask import jsonify
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/payments', methods=['GET'])
def last_payments():
    """return last N payments"""
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    DB_payment.id_payment,
                    DB_payment.id_order,
                    DB_payment.payment,
                    DB_payment.method_payment,
                    DB_payment.data_payment)
                .order_by(DB_payment.id_payment.desc())
                .limit(5))
            payments = session.execute(stmt).all()
            full_block = []
            for row in payments:
                one_block = {"id_payment": row.id_payment,
                             "id_order": row.id_order,
                             "payment": row.payment,
                             "metod_payment": row.method_payment,
                             "data_payment": str(row.data_payment)}
                full_block.insert(0, one_block)
        return jsonify(full_block), 200
    except Exception as e:
        logger.error(f'Error in finance_payments GET: {e}')
        return jsonify(f'Error in finance_payments GET: {e}'), 400
    