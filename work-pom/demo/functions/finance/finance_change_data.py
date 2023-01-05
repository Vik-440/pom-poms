"""Module for changing data in payments and outlays - finished!"""

from sqlalchemy import update
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def payment_changing(id_payment, data):
    """module rof changing data in payment"""
    try:
        with Session(engine)as session:
            stmt = (
                update(db_p)
                .where(db_p.id_payment == id_payment)
                .values(
                    id_order=data['id_order'],
                    payment=data['payment'],
                    metod_payment=data['metod_payment'],
                    data_payment=data['data_payment']))
            session.execute(stmt)
            session.commit()
        return ({"message": "payment_changing excellent"})
    except Exception as e:
        return f'Error in function payment_changing: {e}', 500


def outlay_changing(id_outlay, data):
    """module rof changing data in outlay"""
    try:
        with Session(engine)as session:
            stmt = (
                update(db_ol)
                .where(db_ol.id_outlay == id_outlay)
                .values(
                    data_outlay=data['data_outlay'],
                    id_outlay_class=data['id_outlay_class'],
                    money_outlay=data['money_outlay'],
                    comment_outlay=data['comment_outlay']))
            session.execute(stmt)
            session.commit()
        return ({"message": "outlay_changing excellent"})
    except Exception as e:
        return f'Error in function outlay_changing: {e}', 500
