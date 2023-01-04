import json
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def return_data_from_payment_search(sender):
    with Session(engine) as session:
        data_start = sender['data_start']
        data_end = sender['data_end']
        iban = sender['iban']
        cash = sender['cash']
        if iban and not (cash):
            payment_search_1 = session.query(db_p).filter(
                db_p.data_payment >= data_start,
                db_p.data_payment <= data_end).filter_by(
                    metod_payment="iban").order_by(db_p.data_payment).all()
        elif cash and not (iban):
            payment_search_1 = session.query(db_p).filter(
                db_p.data_payment >= data_start,
                db_p.data_payment <= data_end).filter_by(
                    metod_payment="cash").order_by(db_p.data_payment).all()
        else:
            payment_search_1 = session.query(db_p).filter(
                db_p.data_payment >= data_start,
                db_p.data_payment <= data_end).order_by(
                    db_p.data_payment).all()

        full_block = []
        for row in payment_search_1:
            one_block = {"id_payment": row.id_payment,
                         "id_order": row.id_order,
                         "payment": row.payment,
                         "metod_payment": row.metod_payment,
                         "data_payment": str(row.data_payment)}
            full_block.append(one_block)
    return json.dumps(full_block)


def return_data_from_outlay_search(sender):
    with Session(engine) as session:
        data_start = sender['data_start']
        data_end = sender['data_end']
        full_block = []
        outlay_search_1 = session.query(db_ol).filter(
            db_ol.data_outlay >= data_start,
            db_ol.data_outlay <= data_end).order_by(db_ol.data_outlay).all()
        for row in outlay_search_1:
            one_block = {"id_outlay": row.id_outlay,
                         "data_outlay": str(row.data_outlay),
                         "id_outlay_class": row.id_outlay_class,
                         "money_outlay": row.money_outlay,
                         "comment_outlay": row.comment_outlay}
            full_block.append(one_block)
    return json.dumps(full_block)


def return_data_from_payment_id_order(sender):
    with Session(engine)as session:
        tmp_order = sender['id_order']
        full_block = []
        payment_search_1 = session.query(db_p).filter_by(
            id_order=tmp_order).order_by(db_p.data_payment).all()
        for row in payment_search_1:
            one_block = {"id_payment": row.id_payment,
                         "id_order": row.id_order,
                         "payment": row.payment,
                         "metod_payment": row.metod_payment,
                         "data_payment": str(row.data_payment)}
            full_block.append(one_block)
    return json.dumps(full_block)
