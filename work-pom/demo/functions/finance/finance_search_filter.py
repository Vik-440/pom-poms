"""Module for functions for searching in finance DB - finished!"""

import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def payment_searching(data):
    """Search payments with filters (data and methods)"""
    try:
        with Session(engine) as session:
            data_start = data['data_start']
            data_end = data['data_end']
            iban = data['iban']
            cash = data['cash']
            select_block = select(
                db_p.id_payment,
                db_p.id_order,
                db_p.payment,
                db_p.metod_payment,
                db_p.data_payment)
            if iban and not (cash):
                stmt = (
                    select_block
                    .where(db_p.data_payment >= data_start,
                           db_p.data_payment <= data_end,
                           db_p.metod_payment == 'iban')
                    .order_by(db_p.data_payment))
            elif cash and not (iban):
                stmt = (
                    select_block
                    .where(db_p.data_payment >= data_start,
                           db_p.data_payment <= data_end,
                           db_p.metod_payment == 'cash')
                    .order_by(db_p.data_payment))
            else:
                stmt = (
                    select_block
                    .where(db_p.data_payment >= data_start,
                           db_p.data_payment <= data_end)
                    .order_by(db_p.data_payment))
            payments = session.execute(stmt).all()
            full_block = []
            for row in payments:
                one_block = {"id_payment": row.id_payment,
                             "id_order": row.id_order,
                             "payment": row.payment,
                             "metod_payment": row.metod_payment,
                             "data_payment": str(row.data_payment)}
                full_block.append(one_block)
        return json.dumps(full_block)
    except Exception as e:
        return f'Error in function payment_searching: {e}', 500


def outlay_searching(data):
    """Search outlays with filters"""
    try:
        with Session(engine) as session:
            data_start = data['data_start']
            data_end = data['data_end']
            select_block = select(
                db_ol.id_outlay,
                db_ol.data_outlay,
                db_ol.id_outlay_class,
                db_ol.money_outlay,
                db_ol.comment_outlay)
            stmt = (
                select_block
                .where(db_ol.data_outlay >= data_start,
                       db_ol.data_outlay <= data_end)
                .order_by(db_ol.data_outlay))
            outlays = session.execute(stmt).all()
            full_block = []
            for row in outlays:
                one_block = {"id_outlay": row.id_outlay,
                             "data_outlay": str(row.data_outlay),
                             "id_outlay_class": row.id_outlay_class,
                             "money_outlay": row.money_outlay,
                             "comment_outlay": row.comment_outlay}
                full_block.append(one_block)
        return json.dumps(full_block)
    except Exception as e:
        return f'Error in function outlay_searching: {e}', 500


def payment_id_order_searching(data):
    """Search payments by id order"""
    try:
        with Session(engine)as session:
            id_order = data['id_order']
            select_block = select(
                db_p.id_payment,
                db_p.id_order,
                db_p.payment,
                db_p.metod_payment,
                db_p.data_payment)
            stmt = (
                select_block
                .where(db_p.id_order == id_order)
                .order_by(db_p.data_payment))
            payments = session.execute(stmt).all()
            full_block = []
            for row in payments:
                one_block = {"id_payment": row.id_payment,
                             "id_order": row.id_order,
                             "payment": row.payment,
                             "metod_payment": row.metod_payment,
                             "data_payment": str(row.data_payment)}
                full_block.append(one_block)
        return json.dumps(full_block)
    except Exception as e:
        return f'Error in function payment_id_order_searching: {e}', 500
