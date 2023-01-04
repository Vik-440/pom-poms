"""Returnig last N payments and outlays for starting fin page - finished!"""

import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def opening_last_payments():
    """return last N payments"""
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    db_p.id_payment,
                    db_p.id_order,
                    db_p.payment,
                    db_p.metod_payment,
                    db_p.data_payment)
                .order_by(db_p.id_payment.desc())
                .limit(5))
            payments = session.execute(stmt).all()
            full_block = []
            for row in payments:
                one_block = {"id_payment": row.id_payment,
                             "id_order": row.id_order,
                             "payment": row.payment,
                             "metod_payment": row.metod_payment,
                             "data_payment": str(row.data_payment)}
                full_block.insert(0, one_block)
        return json.dumps(full_block)
    except Exception as e:
        return f'Error in function opening_last_payments: {e}', 500


def opening_last_outlays():
    """return last N outlays"""
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    db_ol.id_outlay,
                    db_ol.data_outlay,
                    db_ol.id_outlay_class,
                    db_ol.money_outlay,
                    db_ol.comment_outlay)
                .order_by(db_ol.id_outlay.desc())
                .limit(5))
            outlays = session.execute(stmt).all()
            full_block = []
            for row in outlays:
                one_block = {"id_outlay": row.id_outlay,
                             "data_outlay": str(row.data_outlay),
                             "id_outlay_class": row.id_outlay_class,
                             "money_outlay": row.money_outlay,
                             "comment_outlay": row.comment_outlay}
                full_block.insert(0, one_block)
        return json.dumps(full_block)
    except Exception as e:
        return f'Error in function opening_last_outlays: {e}', 500
