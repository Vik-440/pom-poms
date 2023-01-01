from sqlalchemy.orm import Session
from db.models import directory_of_order as db_o
from db.models import engine


def change_phase_order_put(id_order, inform):
    """Module for changing phases in order"""
    with Session(engine) as session:
        check_sum = 0
        if 'phase_1' in inform:
            phase_int = inform['phase_1']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(db_o).filter(
                    db_o.id_order == id_order).update({
                        "phase_1": phase_int})
        elif 'phase_2' in inform:
            phase_int = inform['phase_2']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(db_o).filter(
                    db_o.id_order == id_order).update({
                        "phase_2": phase_int})
        elif 'phase_3' in inform:
            phase_int = inform['phase_3']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(db_o).filter(
                    db_o.id_order == id_order).update({
                        "phase_3": phase_int})
        else:
            one_block = {"phase_chenged": "error"}
            return one_block

        session.commit()
        one_block = {"check_sum_phase": check_sum}
    return one_block
