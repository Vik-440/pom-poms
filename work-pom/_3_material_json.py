import json 
from sqlalchemy import MetaData, false, func, true, text, Integer, String, Table, Column, insert, create_engine, \
        and_, or_, update
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine


def return_data_from_material(search):
    with Session(engine) as session:
        j_id_color=[]
        j_name_color=[]
        j_width_color=[]
        j_bab_quantity_color=[]
        j_weight_color=[]
        j_comment_color=[]
        j_bab_weight_color=[]
        # if search ==999 or search==0:
        if search == 999:
            # None
            material_1=session.query(directory_of_color).all()
        elif search == 0:
            # None
            material_1=session.query(directory_of_color).filter(directory_of_color.weight_color > 0).all()
        for row in material_1:
            j_id_color.append(row.id_color)
            j_name_color.append(row.name_color)
            j_width_color.append(row.width_color)
            j_bab_quantity_color.append(row.bab_quantity_color)
            j_weight_color.append(row.weight_color)
            j_comment_color.append(row.comment_color)
            j_bab_weight_color.append(row.bab_weight_color)
            
        a1a=len(j_id_color)
        full_block=[]
        while a1a > 0:
            a1a-=1
            element_1=j_id_color[0]
            del j_id_color[0]
            element_2=j_name_color[0]
            del j_name_color[0]
            element_3=j_width_color[0]
            del j_width_color[0]
            element_4=j_bab_quantity_color[0]
            del j_bab_quantity_color[0]
            element_5=j_weight_color[0]
            del j_weight_color[0]
            element_6=j_comment_color[0]
            del j_comment_color[0]
            element_7=j_bab_weight_color[0]
            del j_bab_weight_color[0]
            element_5=element_5-(element_4 * element_7)

            one_block = {"name_color": element_2, "id_color": element_1, "width_color" : element_3,
                "bab_quantity_color" : element_4, "weight_color" : element_5, "comment_color" : element_6}

            full_block.append(one_block)
    # data_material={"testdata" : "Test-GET-OK"}
    return json.dumps(full_block)       #, ensure_ascii=False, sort_keys = True

############################################################################################################
def return_data_from_material_one(search):
    with Session(engine) as session:
        tmp_id_color=search['id_color']
        # print(tmp_id_color)
        mat=session.query(directory_of_color).filter_by(id_color=tmp_id_color).all()
        for row in mat:
            j_id_color=row.id_color
            j_name_color=row.name_color
            j_width_color=row.width_color
            j_bab_quantity_color=row.bab_quantity_color
            j_weight_color=row.weight_color
            j_comment_color=row.comment_color
            j_thickness_color=row.thickness_color
            j_bab_weight_color=row.bab_weight_color
            j_manufacturer_color=row.manufacturer_color
            j_reserve_color=row.reserve_color
            j_weight_10m_color=row.weight_10m_color

        full_block = {"id_color":j_id_color, "name_color": j_name_color, "width_color" :j_width_color,
                    "bab_quantity_color" :j_bab_quantity_color, "weight_color" :j_weight_color,
                    "comment_color" : j_comment_color,"thickness_color":j_thickness_color,
                    "bab_weight_color":j_bab_weight_color, "manufacturer_color":j_manufacturer_color,
                    "reserve_color":j_reserve_color,"weight_10m_color":j_weight_10m_color}

    return json.dumps(full_block)

############################################################################################################
def return_data_from_material_new(search):
    with Session(engine) as session:
        tmp_id_color=search['color_new']
        if tmp_id_color==0:
            ins = directory_of_color(
                # id_color=4,
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
            j_id_color=ins.id_color
            one_block = {"id_color":j_id_color}
            return one_block
############################################################################################################
def return_data_from_material_change(search):
    with Session(engine) as session:
        tmp_id_color=search['color_change']
        tmp_color=session.query(directory_of_color).filter_by(id_color=tmp_id_color)
        for row in tmp_color:
            tmp_bab=row.bab_quantity_color + search['bab_quantity_color']
            tmp_weight=row.weight_color + search['weight_color']
        rows=session.query(directory_of_color).filter_by(id_color=tmp_id_color).update({'bab_quantity_color':tmp_bab, \
            'weight_color':tmp_weight})
        session.commit()

        one_block = {"color_change": "ok"}
    return one_block
############################################################################################################
def return_data_from_material_change_full(search):
    with Session(engine) as session:
        tmp_id_color=search['color_change_full']
        name_color=search['name_color'],
        width_color=search['width_color'],
        bab_quantity_color=search['bab_quantity_color'],
        weight_color=search['weight_color'],
        comment_color=search['comment_color'],
        thickness_color=search['thickness_color'],
        bab_weight_color=search['bab_weight_color'],
        manufacturer_color=search['manufacturer_color'],
        reserve_color=search['reserve_color'],
        weight_10m_color=search['weight_10m_color']

        rows=session.query(directory_of_color).filter_by(id_color=tmp_id_color).update({'name_color':name_color,
            'width_color':width_color, 'bab_quantity_color':bab_quantity_color, 'weight_color':weight_color,
            'comment_color':comment_color, 'thickness_color':thickness_color, 'bab_weight_color':bab_weight_color,
            'manufacturer_color':manufacturer_color, 'reserve_color':reserve_color, 'weight_10m_color':weight_10m_color})
        session.commit()

        one_block = {"color_change": "ok"}
        return one_block


