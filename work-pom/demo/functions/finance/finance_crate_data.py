from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def return_data_from_payment(sender):
    try:
        with Session(engine) as session:
            z1 = db_p(
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
            z1 = db_ol(
                data_outlay=sender['data_outlay'],
                id_outlay_class=sender['id_outlay_class'],
                money_outlay=sender['money_outlay'],
                comment_outlay=sender['comment_outlay'])
            session.add(z1)
            session.commit()
        return ({"outlay_set": "ok"})
    except Exception as e:
        return f'Error in function finance: {e}', 500
