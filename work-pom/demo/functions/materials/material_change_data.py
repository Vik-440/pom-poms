import json
from sqlalchemy.orm import Session
from db.models import directory_of_color as db_o
from db.models import engine


def changing_material_one(search):
    """Module for fast changing materials"""
    with Session(engine) as session:
        tmp_id_color = search['color_change']
        tmp_color = (session
            .query(db_o)
            .filter_by(id_color=tmp_id_color)
            .all())
        for row in tmp_color:
            tmp_bab = row.bab_quantity_color + search['bab_quantity_color']
            tmp_weight = row.weight_color + search['weight_color']
        session.query(db_o).filter_by(
            id_color=tmp_id_color).update({
                'bab_quantity_color': tmp_bab,
                'weight_color': tmp_weight})
        session.commit()

        one_block = {"color_change": "ok"}
    return one_block


def changing_material_full(search):
    """Module for full changing one material"""
    with Session(engine) as session:
        tmp_id_color = search['color_change_full']
        name_color = search['name_color'],
        width_color = search['width_color'],
        bab_quantity_color = search['bab_quantity_color'],
        weight_color = search['weight_color'],
        comment_color = search['comment_color'],
        thickness_color = search['thickness_color'],
        bab_weight_color = search['bab_weight_color'],
        manufacturer_color = search['manufacturer_color'],
        reserve_color = search['reserve_color'],
        weight_10m_color = search['weight_10m_color']

        session.query(db_o).filter_by(
            id_color=tmp_id_color).update(
                {'name_color': name_color,
                 'width_color': width_color,
                 'bab_quantity_color': bab_quantity_color,
                 'weight_color': weight_color,
                 'comment_color': comment_color,
                 'thickness_color': thickness_color,
                 'bab_weight_color': bab_weight_color,
                 'manufacturer_color': manufacturer_color,
                 'reserve_color': reserve_color,
                 'weight_10m_color': weight_10m_color})
        session.commit()

        one_block = {"color_change": "ok"}
    return one_block
