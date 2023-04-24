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
# @swag_from('/docs/post_payment.yml')
def creating_payment():
    """Create new payment"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/payment(POST) - format json is not correct')
        return jsonify({'payment(POST)': 'json format is not correct'}), 400
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
        return jsonify({"payment": "creating_payment is excellent"}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function finance: {e}') # pragma: no cover
        return f'Error in function finance: {e}', 400 # pragma: no cover
    

@api.route('/finance/payment/<int:id_payment>', methods=['PUT'])
# @swag_from('/docs/put_payment.yml')
def edit_payment(id_payment):
    """module rof changing data in payment"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/payment(PUT) - format json is not correct')
        return jsonify({'payment(PUT)': 'json format is not correct'}), 400
    error_payment = validate_payment(data)
    if error_payment:
        logger.error(f'{error_payment}')
        return jsonify(error_payment), 400
    try:
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
        return jsonify({"payment": "payment changing excellent"}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function finance: {e}') # pragma: no cover
        return f'Error in function finance: {e}', 400 # pragma: no cover


@api.route('/finance/order_payments', methods=['POST'])
# @swag_from('/docs/get_payments.yml')
def payment_id_order_searching():
    """Search payments by id order"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/order_payments(POST) - format json is not correct')
        return jsonify({'order_payments(POST)': 'json format is not correct'}), 400
    try:
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
    except Exception as e: # pragma: no cover
        logger.error(f'Error in finance_payments_order POST: {e}') # pragma: no cover
        return f'Error in order_payments POST: {e}', 400 # pragma: no cover



@api.route('/finance/payments', methods=['GET'])
# @swag_from('/docs/get_payments.yml')
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
    except Exception as e: # pragma: no cover
        logger.error(f'Error in finance_payments GET: {e}')  # pragma: no cover
        return jsonify(f'Error in finance_payments GET: {e}'), 400  # pragma: no cover