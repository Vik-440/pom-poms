"""Module for count and create ctatistic (need refactor to SQLalchemy 2.0)"""

from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app.outlay.validator import validate_balance
from werkzeug.exceptions import BadRequest
from app import engine
from .. import api
from log.logger import logger


def extracting_payment_balans(data):
    """Extracting data for creating balance in finance"""
    try:
        with Session(engine)as session:
            time_period_str = data['balans']
            data_start = data['data_start']
            data_end = data['data_end']
            iban = data['iban']
            cash = data['cash']
            full_block, payment, metod_payment = [], [], []

            data_start_obj = datetime.strptime(data_start, '%Y-%m-%d')
            data_end_obj = datetime.strptime(
                data_end, '%Y-%m-%d') + timedelta(days=1)

            days = data_end_obj - data_start_obj
            day = days.days

            if time_period_str == "day":
                time_step = timedelta(days=1)
                step_day = 1
                data_start_sql = data_start_obj
                data_end_sql = data_start_obj
            elif time_period_str == "week":
                time_step = timedelta(days=7)
                step_day = 7
                data_start_sql = data_start_obj
                data_end_sql = data_start_sql+timedelta(days=6)
            elif time_period_str == "month":
                time_step = timedelta(days=30.5)
                step_day = 30.5
                data_start_sql = data_start_obj
                data_end_sql = data_start_sql+timedelta(days=29.5)
            elif time_period_str == "quarter":
                time_step = timedelta(days=91.5)
                step_day = 91.5
                data_start_sql = data_start_obj
                data_end_sql = data_start_sql+timedelta(days=90.5)
            else:
                time_step = timedelta(days=365)
                step_day = 365
                data_start_sql = data_start_obj
                data_end_sql = data_start_sql+timedelta(days=364)

            while day > 0:
                if iban and not (cash):
                    metod_payment = 'iban'
                    payment_1 = (session
                        .query(
                            func.sum(DB_payment.payment).label('my_sum'),
                            func.count(DB_payment.payment).label('my_count'))
                        .filter(
                            DB_payment.data_payment >= data_start_sql,
                            DB_payment.data_payment <= data_end_sql,
                            DB_payment.method_payment == "iban")
                        .first())
                elif cash and not (iban):
                    metod_payment = 'cash'
                    payment_1 = (session
                        .query(func.sum(DB_payment.payment).label('my_sum'),
                            func.count(DB_payment.payment).label('my_count'))
                        .filter(
                            DB_payment.data_payment >= data_start_sql,
                            DB_payment.data_payment <= data_end_sql,
                            DB_payment.method_payment == "cash")
                        .first())
                else:
                    metod_payment = 'all'
                    payment_1 = (session
                        .query(func.sum(DB_payment.payment).label('my_sum'),
                            func.count(DB_payment.payment).label('my_count'))
                        .filter(DB_payment.data_payment >= data_start_sql,
                                DB_payment.data_payment <= data_end_sql)
                        .first())
                for _ in payment_1:
                    payment_quantity = payment_1.my_count
                    payment = payment_1.my_sum
                if payment_quantity != 0:
                    one_block = {"data_payment": str(data_start_sql.date()),
                                "metod_payment": metod_payment,
                                "payment_quantity": payment_quantity,
                                "payment": payment}
                    full_block.append(one_block)

                data_start_sql = data_start_sql+time_step
                data_end_sql = data_end_sql+time_step
                day = day-step_day
        return full_block
    except Exception as e: # pragma: no cover
        logger.error(f'Error in finance balans: {e}') # pragma: no cover
        return jsonify(f'Error in finance balans: {e}'), 400 # pragma: no cover


@api.route('/finance/payments/statics', methods=['POST'])
def count_balans():
    """This module is old and need rewrite"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/finance(POST) - format json is not correct')
        return jsonify({'finance(POST)': 'json format is not correct'}), 400
    try:
        if 'balans' in data:
            error_balance = validate_balance(data)
            if error_balance:
                logger.error(f'{error_balance}')
                return jsonify(error_balance), 400
            
            return jsonify(extracting_payment_balans(data)), 200
        else:
            return jsonify({'statics': 'finance POST error'}), 400
    except Exception as e: # pragma: no cover
        logger.error(f'Error in finance payments balans POST: {e}') # pragma: no cover
        return jsonify(f'Error in finance payments statics balans: {e}'), 400 # pragma: no cover
    