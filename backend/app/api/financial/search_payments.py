"""Search payments with filters (data and methods)"""

from datetime import datetime
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app import engine
from .. import api
from log.logger import logger


# def payment_searching(data):
#     """Search payments with filters (data and methods)"""
#     try:
#         with Session(engine) as session:
#             data_start = data['data_start']
#             data_end = data['data_end']
#             iban = data['iban']
#             cash = data['cash']
#             select_block = select(
#                 DB_payment.id_payment,
#                 DB_payment.id_order,
#                 DB_payment.payment,
#                 DB_payment.method_payment,
#                 DB_payment.data_payment)
#             if iban and not (cash):
#                 stmt = (
#                     select_block
#                     .where(DB_payment.data_payment >= data_start,
#                            DB_payment.data_payment <= data_end,
#                            DB_payment.method_payment == 'iban')
#                     .order_by(DB_payment.data_payment))
#             elif cash and not (iban):
#                 stmt = (
#                     select_block
#                     .where(DB_payment.data_payment >= data_start,
#                            DB_payment.data_payment <= data_end,
#                            DB_payment.method_payment == 'cash')
#                     .order_by(DB_payment.data_payment))
#             else:
#                 stmt = (
#                     select_block
#                     .where(DB_payment.data_payment >= data_start,
#                            DB_payment.data_payment <= data_end)
#                     .order_by(DB_payment.data_payment))
#             payments = session.execute(stmt).all()
#             full_block = []
#             for row in payments:
#                 one_block = {"id_payment": row.id_payment,
#                              "id_order": row.id_order,
#                              "payment": row.payment,
#                              "method_payment": row.method_payment,
#                              "data_payment": str(row.data_payment)}
#                 full_block.append(one_block)
#         return jsonify(full_block)
#     except Exception as e:
#         return f'Error in function payment_searching: {e}', 500


@api.route('/finance/payments', methods=['POST'])
def searching_payments():
    """Search payments with filters (data and methods)"""
    try:
        data = request.get_json()
        with Session(engine) as session:
            data_start = data['data_start']
            data_end = data['data_end']
            iban = data['iban']
            cash = data['cash']
            select_block = select(
                DB_payment.id_payment,
                DB_payment.id_order,
                DB_payment.payment,
                DB_payment.method_payment,
                DB_payment.data_payment)
            if iban and not (cash):
                stmt = (
                    select_block
                    .where(DB_payment.data_payment >= data_start,
                           DB_payment.data_payment <= data_end,
                           DB_payment.method_payment == 'iban')
                    .order_by(DB_payment.data_payment))
            elif cash and not (iban):
                stmt = (
                    select_block
                    .where(DB_payment.data_payment >= data_start,
                           DB_payment.data_payment <= data_end,
                           DB_payment.method_payment == 'cash')
                    .order_by(DB_payment.data_payment))
            else:
                stmt = (
                    select_block
                    .where(DB_payment.data_payment >= data_start,
                           DB_payment.data_payment <= data_end)
                    .order_by(DB_payment.data_payment))
            payments = session.execute(stmt).all()
            full_block = []
            for row in payments:
                one_block = {"id_payment": row.id_payment,
                             "id_order": row.id_order,
                             "payment": row.payment,
                             "method_payment": row.method_payment,
                             "data_payment": str(row.data_payment)}
                full_block.append(one_block)
        return jsonify(full_block)
    except Exception as e:
        logger.error(f'Error in finance_payments_search POST: {e}')
        return f'Error in finance_payments POST: {e}', 400
    