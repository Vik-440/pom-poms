"""Module for count and create ctatistic (need refactor to SQLalchemy 2.0)"""

from datetime import datetime, timedelta
import calendar
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.payments.models import DB_payment
from app.outlay.models import DB_outlay
from app import engine
from .. import api
from log.logger import logger


def extracting_payment_balans(data):
    """Extracting data for creating balance in finance"""
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
                        DB_payment.data_payment <= data_end_sql)
                    .filter_by(metod_payment="iban")
                    .first())
            elif cash and not (iban):
                metod_payment = 'cash'
                payment_1 = (session
                    .query(func.sum(DB_payment.payment).label('my_sum'),
                           func.count(DB_payment.payment).label('my_count'))
                    .filter(DB_payment.data_payment >= data_start_sql,
                            DB_payment.data_payment <= data_end_sql)
                    .filter_by(metod_payment="cash")
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
    return jsonify(full_block)


@api.route('/finance/payments/statics', methods=['POST'])
def count_balans():
    try:
        data = request.get_json()
        if 'balans' in data:
            return (extracting_payment_balans(data)), 200
    except Exception as e:
        logger.error(f'Error in finance payments balans POST: {e}')
        return jsonify(f'Error in finance payments statics balans: {e}'), 500
    