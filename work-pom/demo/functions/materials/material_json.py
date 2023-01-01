import json
from sqlalchemy.orm import Session
from db.models import directory_of_color as db_o
from db.models import engine


def return_data_from_material(search):
    with Session(engine) as session:
        if search == 999:
            material_1 = session.query(db_o).order_by(
                'name_color').all()
        elif search == 0:
            material_1 = session.query(db_o).filter(
                db_o.weight_color > 0).order_by(
                    'name_color').all()
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


def return_data_from_material_one(search):
    with Session(engine) as session:
        tmp_id_color = search['id_color']
        mat = session.query(db_o).filter_by(
            id_color=tmp_id_color).all()
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


def return_data_from_material_new(search):
    with Session(engine) as session:
        tmp_id_color = search['color_new']
        if tmp_id_color == 0:
            ins = db_o(
                name_color=search['name_color'],
                width_color=search['width_color'],
                bab_quantity_color=search['bab_quantity_color'],
                weight_color=search['weight_color'],
                comment_color=search['comment_color'],
                thickness_color=search['thickness_color'],
                bab_weight_color=search['bab_weight_color'],
                manufacturer_color=search['manufacturer_color'],
                reserve_color=search['reserve_color'],
                weight_10m_color=search['weight_10m_color'])
            session.add(ins)
            session.commit()
            session.refresh(ins)
            j_id_color = ins.id_color
            one_block = {"id_color": j_id_color}
            return one_block


def return_data_from_material_change(search):
    with Session(engine) as session:
        tmp_id_color = search['color_change']
        tmp_color = session.query(db_o).filter_by(
            id_color=tmp_id_color)
        for row in tmp_color:
            tmp_bab = row.bab_quantity_color + search['bab_quantity_color']
            tmp_weight = row.weight_color + search['weight_color']
        session.query(db_o).filter_by(
            id_color=tmp_id_color).update({
                'bab_quantity_color': tmp_bab, 'weight_color': tmp_weight})
        session.commit()

        one_block = {"color_change": "ok"}
    return one_block


def return_data_from_material_change_full(search):
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
