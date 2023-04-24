"""module for search data in outlay"""

from datetime import datetime, timedelta
import calendar
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased
from werkzeug.exceptions import BadRequest

from app.outlay.models import DB_outlay
from app.payments.models import DB_payment
from app.outlay.validator import validate_search_outlay
from app import engine
from .. import api
from log.logger import logger


def extracting_payment_statistics():
    """main block for forecast module"""
    with Session(engine):
        stat_payment, stat_outlay = [], []
        sql_sum = DB_payment.payment
        sql_data = DB_payment.data_payment
        stat_payment = return_forecast(stat_payment, sql_sum, sql_data)
        sql_sum = DB_outlay.money_outlay
        sql_data = DB_outlay.data_outlay
        stat_outlay = return_forecast(stat_outlay, sql_sum, sql_data)
        full_block = {"stat_payment": stat_payment, "stat_outlay": stat_outlay}
    return full_block


def return_forecast(stat, sql_sum, sql_data):
    """module collecting info from db by data_time"""
    ds = datetime.now()
    dsy = ds.year
    dsm = ds.month
    data_start_sql = ds.isoformat()
    data_end_sql = ds.isoformat()
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)

    time_step = timedelta(days=1)
    data_start_sql = (ds-time_step).strftime('%Y-%m-%d')
    data_end_sql = (ds-time_step).strftime('%Y-%m-%d')
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)
    time_step = timedelta(days=2)
    data_start_sql = (ds-time_step).strftime('%Y-%m-%d')
    data_end_sql = (ds-time_step).strftime('%Y-%m-%d')
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)
    #  this month
    data_start_sql = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    data_end_sql = datetime.today().replace(day=(
        calendar.monthrange(dsy, dsm)[1])).strftime('%Y-%m-%d')
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)
    # privius mohth
    data_start_sql = (((datetime.today()).replace(day=1)-timedelta(
        days=1))).replace(day=1).strftime('%Y-%m-%d')
    data_end_sql = ((datetime.today()).replace(
        day=1)-timedelta(days=1)).strftime('%Y-%m-%d')
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)
    # this year
    data_start_sql = ds.replace(month=1, day=1).strftime('%Y-%m-%d')
    data_end_sql = ds.replace(month=12, day=31).strftime('%Y-%m-%d')
    stat = return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data)
    # forecast this year
    days_year = (ds-ds.replace(month=1, day=1))
    if stat[0] is None:
        stat[0] = 0 # pragma: no cover
    if days_year is None or days_year == 0:
        days_year = 1 # pragma: no cover
    forecast = round((stat[0]/days_year.days)*365)
    stat.insert(0, forecast)

    return (stat)


def return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data):
    """Extracting data frm DB and counting SUM"""
    with Session(engine) as session:
        payment_1 = (session
            .query(func.sum(sql_sum).label('my_sum'))
            .filter(sql_data >= data_start_sql, sql_data <= data_end_sql)
            .first())
        for row in payment_1:
            payment = payment_1.my_sum
        stat.insert(0, payment)
    return (stat)



def outlay_searching(data):
    """Search outlays with filters"""
    try:
        with Session(engine) as session:
            data_start = data['data_start']
            data_end = data['data_end']
            select_block = select(
                DB_outlay.id_outlay,
                DB_outlay.data_outlay,
                DB_outlay.id_outlay_class,
                DB_outlay.money_outlay,
                DB_outlay.comment)
            stmt = (
                select_block
                .where(DB_outlay.data_outlay >= data_start,
                       DB_outlay.data_outlay <= data_end)
                .order_by(DB_outlay.data_outlay))
            outlays = session.execute(stmt).all()
            full_block = []
            for row in outlays:
                one_block = {"id_outlay": row.id_outlay,
                             "data_outlay": str(row.data_outlay),
                             "id_outlay_class": row.id_outlay_class,
                             "money_outlay": row.money_outlay,
                             "comment_outlay": row.comment}
                full_block.append(one_block)
        return full_block
    except Exception as e: # pragma: no cover
        return f'Error in function outlay_searching: {e}', 400 # pragma: no cover


@api.route('/finance', methods=['POST'])
def finance():
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/finance(POST) - format json is not correct')
        return jsonify({'finance(POST)': 'json format is not correct'}), 400
    try:
        if 'outlay_search' in data:
            error_search_outlay = validate_search_outlay(data)
            if error_search_outlay:
                logger.error(f'{error_search_outlay}')
                return jsonify(error_search_outlay), 400
            return jsonify(outlay_searching(data)), 200
        elif 'stat' in data:
            return jsonify(extracting_payment_statistics()), 200
        else:
            return jsonify({'message': 'finance POST error'}), 400
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function finance: {e}') # pragma: no cover
        return f'Error in function finance: {e}', 400 # pragma: no cover
    