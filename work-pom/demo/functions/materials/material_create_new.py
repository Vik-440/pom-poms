import json
from sqlalchemy.orm import Session
from db.models import directory_of_color as db_o
from db.models import engine


def material_creating_new(data):
    """module for create new possition of material"""
    with Session(engine) as session:
        tmp_id_color = data['color_new']
        if tmp_id_color == 0:
            ins = db_o(
                name_color=data['name_color'],
                width_color=data['width_color'],
                bab_quantity_color=data['bab_quantity_color'],
                weight_color=data['weight_color'],
                comment_color=data['comment_color'],
                thickness_color=data['thickness_color'],
                bab_weight_color=data['bab_weight_color'],
                manufacturer_color=data['manufacturer_color'],
                reserve_color=data['reserve_color'],
                weight_10m_color=data['weight_10m_color'])
            session.add(ins)
            session.commit()
            session.refresh(ins)
            j_id_color = ins.id_color
            one_block = {"id_color": j_id_color}
    return one_block
