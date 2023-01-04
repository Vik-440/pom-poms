from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def return_data_from_payment_change(id, sender):
    try:
        with Session(engine)as session:
            id_order = sender['id_order']
            payment = sender['payment']
            metod_payment = sender['metod_payment']
            data_payment = sender['data_payment']
            session.query(db_p).filter_by(
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
            session.query(db_ol).filter_by(
                id_outlay=id).update(
                    {'data_outlay': data_outlay,
                     'id_outlay_class': id_outlay_class,
                     'money_outlay': money_outlay,
                     'comment_outlay': comment_outlay})
            session.commit()
        return ({"id_outlay": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500
