"""Module for extract id_material about materials \
 This file wait refactoring in next stage ! ! ! """

# from datetime import datetime
from flask import request, jsonify
from sqlalchemy import select, update#, func, or_, and_, join, table
from sqlalchemy.orm import Session#, aliased

from app.materials.models import DB_materials
# from app.materials.forms import MaterialForm
from app import engine
from .. import api
from log.logger import logger


def create_select_module():
    select_module = (select(
            DB_materials.id_material,
            DB_materials.name,
            DB_materials.width,
            DB_materials.spool_qty,
            DB_materials.spool_weight,
            DB_materials.weight,
            DB_materials.comment,
            
            DB_materials.article,
            DB_materials.thickness,
            DB_materials.manufacturer,
            DB_materials.reserve,
            DB_materials.weight_10m
            ))
    return select_module


def extracting_material_all(id_material):
    """module for extracting full data from DB"""
    with Session(engine) as session:
        select_module = create_select_module()
        
        if id_material == 999:
            stmt = (select_module.order_by(DB_materials.id_material))
        elif id_material == 0:
            stmt = (
                select_module
                .where(DB_materials.weight > 0)
                .order_by(DB_materials.id_material))
        materials = session.execute(stmt).all()
        
        full_block = []
        for malerial in materials:
            weight = malerial.weight - (
                malerial.spool_qty * malerial.spool_weight)
            full_block.append({
                         "id_color": malerial.id_material,
                         "name_color": malerial.name,
                         "width_color": malerial.width,
                         "bab_quantity_color": malerial.spool_qty,
                         "weight_color": weight,
                         "comment_color": malerial.comment})
    return jsonify(full_block)


def extracting_material_one(id_material):
    """module for full exstracting data of one material"""
    with Session(engine) as session:
        # print(id_material)
        select_module = create_select_module()
        stmt = select_module.where(DB_materials.id_material == id_material)
        material = session.execute(stmt).fetchone()

        if material is None:
            return jsonify({'message': 'This ID material does not exist'}) # pragma: no cover
        full_block = {"id_color": material.id_material,
                        "name_color": material.name,
                        "width_color": material.width,
                        "bab_quantity_color": material.spool_qty,
                        "weight_color": material.weight,
                        "comment_color": material.comment,
                        "thickness_color": material.thickness,
                        "bab_weight_color": material.spool_weight,
                        "manufacturer_color": material.manufacturer,
                        "reserve_color": material.reserve,
                        "weight_10m_color": material.weight_10m}
    return jsonify(full_block)


def creating_new_material(data):
    """module for create new possition of material"""
    id_new_material = None
    with Session(engine) as session:
        if data['color_new'] == 0:
            ins = DB_materials(
                name=data['name_color'],
                width=data['width_color'],
                spool_qty=data['bab_quantity_color'],
                weight=data['weight_color'],
                comment=data['comment_color'],
                thickness=data['thickness_color'],
                spool_weight=data['bab_weight_color'],
                manufacturer=data['manufacturer_color'],
                reserve=data['reserve_color'],
                weight_10m=data['weight_10m_color'])
            session.add(ins)
            session.commit()
            session.refresh(ins)
            id_new_material = ins.id_material
        else:
            return jsonify({'message': 'error in func'}) # pragma: no cover
    return jsonify({"id_color": id_new_material})


def changing_material_one(data):
    """Module for fast changing materials"""
    with Session(engine) as session:
        id_material = data['color_change']
        stmt = (
            select(
                DB_materials.spool_qty,
                DB_materials.weight)
            .where(DB_materials.id_material == id_material))
        material = session.execute(stmt).fetchone()
        spool_sum = material.spool_qty + data['bab_quantity_color']
        weight_sum = material.weight + data['weight_color']

        stmt = (
            update(DB_materials)
            .where(DB_materials.id_material == id_material)
            .values(spool_qty = spool_sum,
                    weight = weight_sum))
        session.execute(stmt)
        session.commit()
    return jsonify({"color_change": "ok"})


def changing_material_full(data):
    """Module for full changing one material"""
    with Session(engine) as session:
        id_material = data['color_change_full']
        stmt = (
            update(DB_materials)
            .where(DB_materials.id_material == id_material)
            .values(
                name = data['name_color'],
                width = data['width_color'],
                spool_qty = data['bab_quantity_color'],
                weight = data['weight_color'],
                comment = data['comment_color'],
                thickness = data['thickness_color'],
                spool_weight = data['bab_weight_color'],
                manufacturer = data['manufacturer_color'],
                reserve = data['reserve_color'],
                weight_10m = data['weight_10m_color']))
        session.execute(stmt)
        session.commit()
    return jsonify({'message': "data_change ok"})



@api.route('/material', methods=['GET'])
def material():
    try:
        return (extracting_material_all(0)), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function material GET: {e}') # pragma: no cover
        return jsonify(f'Error in function material GET: {e}'), 400 # pragma: no cover
    

@api.route('/material', methods=['POST'])
def material_post():
    try:
        request.data = request.get_json()
        if 'id_color' in request.data:
            id_color = request.data['id_color']
            if id_color == 999:
                data = extracting_material_all(999)
            else:
                data = extracting_material_one(id_color)
        elif 'color_new' in request.data:
            data = creating_new_material(request.data)
        elif 'color_change' in request.data:
            data = changing_material_one(request.data)
        elif 'color_change_full' in request.data:
            data = changing_material_full(request.data)
        else:
            data = {"message": "request is not correct"}
        return data, 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function material POST: {e}') # pragma: no cover
        return f'Error in function material POST: {e}', 400 # pragma: no cover
    