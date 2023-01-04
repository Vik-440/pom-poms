"""Module for changing phases of produce"""

from sqlalchemy.orm import Session
from sqlalchemy import update
from db.models import directory_of_order as db_o
from db.models import engine


def changing_order_phases(id_order, data):
    """Module for changing phases in order"""
    with Session(engine) as session:

        if 'phase_1' in data:
            phase_int = data['phase_1']
            stmt = (
                update(db_o)
                .where(db_o.id_order == id_order)
                .values(phase_1=phase_int))
            session.execute(stmt)

        if 'phase_2' in data:
            phase_int = data['phase_2']
            stmt = (
                update(db_o)
                .where(db_o.id_order == id_order)
                .values(phase_2=phase_int))
            session.execute(stmt)

        if 'phase_3' in data:
            phase_int = data['phase_3']
            stmt = (
                update(db_o)
                .where(db_o.id_order == id_order)
                .values(phase_3=phase_int))
            session.execute(stmt)

        session.commit()

        one_block = {"message": "excellent"}
    return one_block
