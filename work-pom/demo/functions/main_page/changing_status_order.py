# import json
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from db.models import directory_of_order as db_o
# from db.models import directory_of_client as db_c
# from db.models import directory_of_payment as db_p
# from db.models import directory_of_model as db_m
from db.models import engine


def changing_status_order(id_order: int, data: bool):
    """Module for changing of fulfilled status"""
    with Session(engine) as session:
        status_order = data['status_order']
        if not status_order:
            stmt = update(db_o).where(
                db_o.id_order == id_order).values(fulfilled_order=False)
        else:
            ds = datetime.today().strftime('%Y-%m-%d')
            stmt = select(db_o.quantity_pars_model).where(
                            db_o.id_order == id_order)
            pre_data = session.execute(stmt).first()
            phaze_to_ziro = []
            for step in pre_data:
                for k in step:
                    phaze_to_ziro.append(0)
            stmt = (
                update(db_o)
                .where(db_o.id_order == id_order)
                .values(
                    fulfilled_order=True,
                    phase_1=phaze_to_ziro,
                    phase_2=phaze_to_ziro,
                    phase_3=phaze_to_ziro,
                    data_plane_order=ds))
        session.execute(stmt)
        session.commit()
        one_block = {"message": "excellent"}
    return one_block
