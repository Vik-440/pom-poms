import json
from sqlalchemy.orm import Session
from db.models import directory_of_payment as db_p
from db.models import directory_of_outlay as db_ol
from db.models import engine


def ret_dat_fin_pay_get():
    """return last N payments"""
    with Session(engine) as session:
        full_block = []
        pay_get = session.query(db_p).order_by(
            db_p.id_payment.desc()).limit(5)
        for row in pay_get:
            one_block = {"id_payment": row.id_payment,
                         "id_order": row.id_order,
                         "payment": row.payment,
                         "metod_payment": row.metod_payment,
                         "data_payment": str(row.data_payment)}
            full_block.insert(0, one_block)
    return json.dumps(full_block)


def ret_dat_fin_out_get():
    """return last N outlays"""
    with Session(engine) as session:
        full_block = []
        pay_get = session.query(db_ol).order_by(
            db_ol.id_outlay.desc()).limit(5)
        for row in pay_get:
            one_block = {"id_outlay": row.id_outlay,
                         "data_outlay": str(row.data_outlay),
                         "id_outlay_class": row.id_outlay_class,
                         "money_outlay": row.money_outlay,
                         "comment_outlay": row.comment_outlay}
            full_block.insert(0, one_block)
    return json.dumps(full_block)
