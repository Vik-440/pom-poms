"""Module for count and create ctatistic and forecast on future - finished!"""
import json
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine
import calendar


def extracting_payment_statistics():
    """main block for forecast module"""
    with Session(engine):
        stat_payment, stat_outlay = [], []
        sql_sum = db_p.payment
        sql_data = db_p.data_payment
        stat_payment = return_forecast(stat_payment, sql_sum, sql_data)
        sql_sum = db_ol.money_outlay
        sql_data = db_ol.data_outlay
        stat_outlay = return_forecast(stat_outlay, sql_sum, sql_data)
        full_block = {"stat_payment": stat_payment, "stat_outlay": stat_outlay}
    return json.dumps(full_block)


def return_forecast(stat, sql_sum, sql_data):
    """module collecting info from db by data_time"""
    ds = datetime.today()
    ds1 = ds.strftime('%Y-%m-%d')
    dsm = ds.strftime('%Y,%m')
    dsy = int(ds.strftime('%Y'))
    dsm = int(ds.strftime('%m'))
    data_start_sql = ds1
    data_end_sql = ds1
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
        stat[0] = 0
    if days_year is None or days_year == 0:
        days_year = 1
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
                        func.sum(db_p.payment).label('my_sum'),
                        func.count(db_p.payment).label('my_count'))
                    .filter(
                        db_p.data_payment >= data_start_sql,
                        db_p.data_payment <= data_end_sql)
                    .filter_by(metod_payment="iban")
                    .first())
            elif cash and not (iban):
                metod_payment = 'cash'
                payment_1 = (session
                    .query(func.sum(db_p.payment).label('my_sum'),
                           func.count(db_p.payment).label('my_count'))
                    .filter(db_p.data_payment >= data_start_sql,
                            db_p.data_payment <= data_end_sql)
                    .filter_by(metod_payment="cash")
                    .first())
            else:
                metod_payment = 'all'
                payment_1 = (session
                    .query(func.sum(db_p.payment).label('my_sum'),
                           func.count(db_p.payment).label('my_count'))
                    .filter(db_p.data_payment >= data_start_sql,
                            db_p.data_payment <= data_end_sql)
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
    return json.dumps(full_block)
