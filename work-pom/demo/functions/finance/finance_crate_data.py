"""Module for create payments and outlays - finished!"""

from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def creating_payment(data):
    try:
        with Session(engine) as session:
            stmt = (
                db_p(
                    id_order=data['id_order'],
                    payment=data['payment'],
                    metod_payment=data['metod_payment'],
                    data_payment=data['data_payment']))
            session.add(stmt)
            session.commit()
        return ({"message": "creating_payment is excellent"})
    except Exception as e:
        return f'Error in function creating_payment: {e}', 500


def creating_outlay(data):
    try:
        with Session(engine) as session:
            stmt = (
                db_ol(
                    data_outlay=data['data_outlay'],
                    id_outlay_class=data['id_outlay_class'],
                    money_outlay=data['money_outlay'],
                    comment_outlay=data['comment_outlay']))
            session.add(stmt)
            session.commit()
        return ({"message": "creating_outlay is excellent"})
    except Exception as e:
        return f'Error in function creating_outlay: {e}', 500
