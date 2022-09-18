import json
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models import directory_of_payment
from db.models import directory_of_outlay  #, directory_of_outlay_class
from db.models import engine
import calendar


# def return_data_from_finance(asked):
#     with Session(engine) as session:
#         data_outlay_class = []
#         id_payment = []
#         id_order = []
#         payment = []
#         metod_payment = []
#         data_payment = []
#         full_block = []
#         id_outlay = []
#         data_outlay = []
#         id_outlay_class = []
#         money_outlay = []
#         comment_outlay = []
#         data_outlay_class_1 = session.query(directory_of_outlay_class).all()
#         for row in data_outlay_class_1:
#             data_outlay_class.append(row.outlay_class)
#         data_last_payment_1 = session.query(directory_of_payment).order_by(
#             directory_of_payment.id_payment.desc()).limit(3)
#         for row in data_last_payment_1:
#             id_payment.append(row.id_payment)
#             id_order.append(row.id_order)
#             payment.append(row.payment)
#             metod_payment.append(row.metod_payment)
#             data_payment.append(str(row.data_payment))
#         data_last_outlay_1 = session.query(directory_of_outlay).order_by(
#             directory_of_outlay.id_outlay.desc()).limit(3)
#         for row in data_last_outlay_1:
#             id_outlay.append(row.id_outlay)
#             data_outlay.append(str(row.data_outlay))
#             id_outlay_class.append(row.id_outlay_class)
#             money_outlay.append(row.money_outlay)
#             comment_outlay.append(row.comment_outlay)

#         one_block = {"metod_payment": ["iban", "cash"],
#                      "outlay_class": data_outlay_class}
#         full_block.append(one_block)

#         q1 = block_json(id_payment, id_order, payment, metod_payment,
#                         data_payment)
#         q11 = {"id_payment": q1[0], "id_order": q1[1], "payment": q1[2],
#                "metod_payment": q1[3], "data_payment": q1[4]}
#         q1 = block_json(id_payment, id_order, payment, metod_payment,
#                         data_payment)
#         q12 = {"id_payment": q1[0], "id_order": q1[1], "payment": q1[2],
#                "metod_payment": q1[3], "data_payment": q1[4]}
#         q1 = block_json(id_payment, id_order, payment, metod_payment,
#                         data_payment)
#         q13 = {"id_payment": q1[0], "id_order": q1[1], "payment": q1[2],
#                "metod_payment": q1[3], "data_payment": q1[4]}
#         full_block.append(q13)
#         full_block.append(q12)
#         full_block.append(q11)

#         q4 = block_json(id_outlay, data_outlay, id_outlay_class, money_outlay,
#                         comment_outlay)
#         one_block1 = {"id_outlay": q4[0], "data_outlay": q4[1],
#                       "id_outlay_class": q4[2], "money_outlay": q4[3],
#                       "comment_outlay": q4[4]}
#         q4 = block_json(id_outlay, data_outlay, id_outlay_class, money_outlay,
#                         comment_outlay)
#         one_block2 = {"id_outlay": q4[0], "data_outlay": q4[1],
#                       "id_outlay_class": q4[2], "money_outlay": q4[3],
#                       "comment_outlay": q4[4]}
#         q4 = block_json(id_outlay, data_outlay, id_outlay_class, money_outlay,
#                         comment_outlay)
#         one_block3 = {"id_outlay": q4[0], "data_outlay": q4[1],
#                       "id_outlay_class": q4[2], "money_outlay": q4[3],
#                       "comment_outlay": q4[4]}

#         full_block.append(one_block3)
#         full_block.append(one_block2)
#         full_block.append(one_block1)
#     return json.dumps(full_block)


def return_data_from_payment(sender):
    try:
        with Session(engine) as session:
            z1 = directory_of_payment(
                id_order=sender['id_order'],
                payment=sender['payment'],
                metod_payment=sender['metod_payment'],
                data_payment=sender['data_payment'])
            session.add(z1)
            session.commit()
        return ({"payment_set": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500


def return_data_from_outlay(sender):
    try:
        with Session(engine) as session:
            z1 = directory_of_outlay(
                data_outlay=sender['data_outlay'],
                id_outlay_class=sender['id_outlay_class'],
                money_outlay=sender['money_outlay'],
                comment_outlay=sender['comment_outlay'])
            session.add(z1)
            session.commit()
        return ({"outlay_set": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500


def return_data_from_payment_search(sender):
    with Session(engine) as session:
        data_start = sender['data_start']
        data_end = sender['data_end']
        iban = sender['iban']
        cash = sender['cash']
        if iban and not (cash):
            payment_search_1 = session.query(directory_of_payment).filter(
                directory_of_payment.data_payment >= data_start,
                directory_of_payment.data_payment <= data_end).filter_by(
                    metod_payment="iban").all()
        elif cash and not (iban):
            payment_search_1 = session.query(directory_of_payment).filter(
                directory_of_payment.data_payment >= data_start,
                directory_of_payment.data_payment <= data_end).filter_by(
                    metod_payment="cash").all()
        else:
            payment_search_1 = session.query(directory_of_payment).filter(
                directory_of_payment.data_payment >= data_start,
                directory_of_payment.data_payment <= data_end).all()

        full_block, id_payment, id_order, payment, metod_payment, \
            data_payment = [], [], [], [], [], []
        for row in payment_search_1:
            id_payment.append(row.id_payment)
            id_order.append(row.id_order)
            payment.append(row.payment)
            metod_payment.append(row.metod_payment)
            data_payment.append(str(row.data_payment))
        a1a = len(id_payment)
        while a1a > 0:
            a1a -= 1
            q1 = block_json(id_payment, id_order, payment, metod_payment,
                            data_payment)
            one_block = {"id_payment": q1[0], "id_order": q1[1],
                         "payment": q1[2], "metod_payment": q1[3],
                         "data_payment": q1[4]}
            full_block.append(one_block)
    return json.dumps(full_block)


def return_data_from_outlay_search(sender):
    with Session(engine) as session:
        data_start = sender['data_start']
        data_end = sender['data_end']
        full_block, id_outlay, data_outlay, id_outlay_class, money_outlay,\
            comment_outlay = [], [], [], [], [], []
        outlay_search_1 = session.query(directory_of_outlay).filter(
            directory_of_outlay.data_outlay >= data_start,
            directory_of_outlay.data_outlay <= data_end).all()
        for row in outlay_search_1:
            id_outlay.append(row.id_outlay)
            data_outlay.append(str(row.data_outlay))
            id_outlay_class.append(row.id_outlay_class)
            money_outlay.append(row.money_outlay)
            comment_outlay.append(row.comment_outlay)
        a1a = len(id_outlay)
        while a1a > 0:
            a1a -= 1
            q4 = block_json(id_outlay, data_outlay, id_outlay_class,
                            money_outlay, comment_outlay)
            one_block = {"id_outlay": q4[0], "data_outlay": q4[1],
                         "id_outlay_class": q4[2], "money_outlay": q4[3],
                         "comment_outlay": q4[4]}
            full_block.append(one_block)
    return json.dumps(full_block)


def return_data_from_payment_change(id, sender):
    try:
        with Session(engine)as session:
            id_order = sender['id_order']
            payment = sender['payment']
            metod_payment = sender['metod_payment']
            data_payment = sender['data_payment']
            session.query(directory_of_payment).filter_by(
                id_payment=id).update(
                    {'id_order': id_order, 'payment': payment,
                     'metod_payment': metod_payment,
                     'data_payment': data_payment})
            session.commit()
        return ({"id_payment": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500


def return_data_from_outlay_change(id, sender):
    try:
        with Session(engine)as session:
            data_outlay = sender['data_outlay']
            id_outlay_class = sender['id_outlay_class']
            money_outlay = sender['money_outlay']
            comment_outlay = sender['comment_outlay']
            session.query(directory_of_outlay).filter_by(
                id_outlay=id).update(
                    {'data_outlay': data_outlay,
                     'id_outlay_class': id_outlay_class,
                     'money_outlay': money_outlay,
                     'comment_outlay': comment_outlay})
            session.commit()
        return ({"id_outlay": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500


def return_data_from_payment_id_order(sender):
    with Session(engine)as session:
        tmp_order = sender['id_order']
        full_block, id_payment, id_order, payment, metod_payment, data_payment\
            = [], [], [], [], [], []
        payment_search_1 = session.query(directory_of_payment).filter_by(
            id_order=tmp_order).all()
        for row in payment_search_1:
            id_payment.append(row.id_payment)
            id_order.append(row.id_order)
            payment.append(row.payment)
            metod_payment.append(row.metod_payment)
            data_payment.append(str(row.data_payment))
        a1a = len(id_payment)
        while a1a > 0:
            a1a -= 1
            q1 = block_json(id_payment, id_order, payment, metod_payment,
                            data_payment)
            one_block = {"id_payment": q1[0], "id_order": q1[1],
                         "payment": q1[2], "metod_payment": q1[3],
                         "data_payment": q1[4]}
            full_block.append(one_block)
    return json.dumps(full_block)


def return_data_from_payment_balans(sender):
    with Session(engine)as session:
        time_period_str = sender['balans']
        data_start = sender['data_start']
        data_end = sender['data_end']
        iban = sender['iban']
        cash = sender['cash']
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
                payment_1 = session.query(
                    func.sum(directory_of_payment.payment).label('my_sum'),
                    func.count(
                        directory_of_payment.payment).label(
                        'my_count')).filter(
                    directory_of_payment.data_payment >= data_start_sql,
                    directory_of_payment.data_payment <= data_end_sql
                    ).filter_by(metod_payment="iban").first()
            elif cash and not (iban):
                metod_payment = 'cash'
                payment_1 = session.query(
                    func.sum(directory_of_payment.payment).label('my_sum'),
                    func.count(directory_of_payment.payment).label('my_count')
                    ).filter(
                    directory_of_payment.data_payment >= data_start_sql,
                    directory_of_payment.data_payment <= data_end_sql
                    ).filter_by(metod_payment="cash").first()
            else:
                metod_payment = 'all'
                payment_1 = session.query(
                    func.sum(directory_of_payment.payment).label('my_sum'),
                    func.count(directory_of_payment.payment).label('my_count')
                    ).filter(
                    directory_of_payment.data_payment >= data_start_sql,
                    directory_of_payment.data_payment <= data_end_sql).first()
            for row in payment_1:
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
        # full_block={"testdata" : "in progres"}
    return json.dumps(full_block)


def return_data_from_payment_stat(search):
    with Session(engine):
        # as session:
        stat, stat_outlay = [], []

        sql_sum = directory_of_payment.payment
        sql_data = directory_of_payment.data_payment
        stat_payment = return_forecast(stat, sql_sum, sql_data)

        sql_sum = directory_of_outlay.money_outlay
        sql_data = directory_of_outlay.data_outlay
        stat_outlay = return_forecast(stat_outlay, sql_sum, sql_data)

        full_block = {"stat_payment": stat_payment, "stat_outlay": stat_outlay}
    return json.dumps(full_block)

# work here now #


def return_forecast(stat, sql_sum, sql_data):
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
    forecast = round((stat[0]/days_year.days)*365)
    stat.insert(0, forecast)

    return (stat)


def return_stat(data_start_sql, data_end_sql, stat, sql_sum, sql_data):
    with Session(engine) as session:
        payment_1 = session.query(func.sum(sql_sum).label('my_sum')).filter(
                sql_data >= data_start_sql, sql_data <= data_end_sql).first()
        for row in payment_1:
            payment = payment_1.my_sum
        stat.insert(0, payment)
    return (stat)


def ret_dat_fin_pay_get():
    with Session(engine) as session:
        id_payment, id_order, payment = [], [], []
        metod_payment, data_payment, full_block = [], [], []
        pay_get = session.query(directory_of_payment).order_by(
            directory_of_payment.id_payment.desc()).limit(3)
        for row in pay_get:
            id_payment.append(row.id_payment)
            id_order.append(row.id_order)
            payment.append(row.payment)
            metod_payment.append(row.metod_payment)
            data_payment.append(str(row.data_payment))
        numb = 0
        while numb < len(id_payment):
            one_block = {"id_payment": id_payment[numb],
                         "id_order": id_order[numb],
                         "payment": payment[numb],
                         "metod_payment": metod_payment[numb],
                         "data_payment": data_payment[numb]}
            full_block.insert(0, one_block)
            numb += 1
    return json.dumps(full_block)


def ret_dat_fin_out_get():
    with Session(engine) as session:
        id_outlay, data_outlay, id_outlay_class = [], [], []
        money_outlay, comment_outlay, full_block = [], [], []
        pay_get = session.query(directory_of_outlay).order_by(
            directory_of_outlay.id_outlay.desc()).limit(3)
        for row in pay_get:
            id_outlay.append(row.id_outlay)
            data_outlay.append(str(row.data_outlay))
            id_outlay_class.append(row.id_outlay_class)
            money_outlay.append(row.money_outlay)
            comment_outlay.append(row.comment_outlay)
        numb = 0
        while numb < len(id_outlay):
            one_block = {"id_outlay": id_outlay[numb],
                         "data_outlay": data_outlay[numb],
                         "id_outlay_class": id_outlay_class[numb],
                         "money_outlay": money_outlay[numb],
                         "comment_outlay": comment_outlay[numb]}
            full_block.insert(0, one_block)
            numb += 1
    return json.dumps(full_block)


def block_json(pos1, pos2, pos3, pos4, pos5):
    el1 = pos1[0]
    del pos1[0]
    el2 = pos2[0]
    del pos2[0]
    el3 = pos3[0]
    del pos3[0]
    el4 = pos4[0]
    del pos4[0]
    el5 = pos5[0]
    del pos5[0]
    return [el1, el2, el3, el4, el5]
