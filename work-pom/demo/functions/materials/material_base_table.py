import json
from sqlalchemy.orm import Session
from db.models import directory_of_color as db_o
from db.models import engine


def extracting_material_all(data):
    """module for extracting full data from DB"""
    with Session(engine) as session:
        if data == 999:
            material_1 = (session
                .query(db_o)
                .order_by('name_color')
                .all())
        elif data == 0:
            material_1 = (session
                .query(db_o)
                .filter(db_o.weight_color > 0)
                .order_by('name_color')
                .all())
        full_block = []
        for row in material_1:
            weight_color = row.weight_color - (
                row.bab_quantity_color * row.bab_weight_color)
            one_block = {
                         "id_color": row.id_color,
                         "name_color": row.name_color,
                         "width_color": row.width_color,
                         "bab_quantity_color": row.bab_quantity_color,
                         "weight_color": weight_color,
                         "comment_color": row.comment_color}
            full_block.append(one_block)
    return json.dumps(full_block)


def extracting_material_one(data):
    """module for full exstracting data of one material"""
    with Session(engine) as session:
        tmp_id_color = data['id_color']
        mat = (session
            .query(db_o)
            .filter_by(id_color=tmp_id_color)
            .all())
        for row in mat:
            full_block = {"id_color": row.id_color,
                          "name_color": row.name_color,
                          "width_color": row.width_color,
                          "bab_quantity_color": row.bab_quantity_color,
                          "weight_color": row.weight_color,
                          "comment_color": row.comment_color,
                          "thickness_color": row.thickness_color,
                          "bab_weight_color": row.bab_weight_color,
                          "manufacturer_color": row.manufacturer_color,
                          "reserve_color": row.reserve_color,
                          "weight_10m_color": row.weight_10m_color}
    return json.dumps(full_block)
