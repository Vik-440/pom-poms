"""Module routes with materials"""

from flask import request, jsonify
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from typing import List, Dict
from werkzeug.exceptions import BadRequest
from flasgger import swag_from

from app.materials.models import DB_materials
from app.materials.validator import (
    validate_id_material,
    validate_material,
    validate_new_name_material,
    errors_validate_consumption)
from app import engine
from .. import api
from log.logger import logger


@api.route('/materials', methods=['POST'])
@swag_from('/docs/post_material.yml')
def create_material() -> dict:
    """create material"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/materials(POST) - format json is not correct')
        return jsonify({'materials': 'json format is not correct'}), 400

    errors_validate = validate_material(data)
    if errors_validate:
        logger.error(f'{errors_validate}')
        return jsonify(errors_validate), 400

    error_new_name = validate_new_name_material(data)
    if error_new_name:
        logger.error(f'{error_new_name}')
        return jsonify(error_new_name), 400

    try:
        with Session(engine) as session:
            stmt = (func.max(DB_materials.id_material))
            id_max_material = session.execute(stmt).scalar()
            id_material = id_max_material + 1 if id_max_material is not None else 1  # noqa
            stmt = DB_materials(
                id_material=id_material,
                comment=data['comment'],
                manufacturer=data['manufacturer'],
                name=data['name'],
                reserve=data['reserve'],
                spool_qty=data['spool_qty'],
                spool_weight=data['spool_weight'],
                thickness=data['thickness'],
                weight=data['weight'],
                weight_10m=data['weight_10m'],
                width=data['width'])
            session.add(stmt)
            session.commit()
            session.refresh(stmt)
            if id_material == stmt.id_material:
                return jsonify({'id_material': id_material}), 201
            else:  # pragma: no cover
                raise ValueError  # pragma: no cover
    except Exception as e:  # pragma: no cover
        logger.error({'materials_(POST)': e})
        return jsonify({'materials_(POST)': e}), 400


@api.route('/materials', methods=['GET'])
@swag_from('/docs/get_materials.yml')
def materials() -> List[Dict]:
    """read materials in general"""
    available = request.args.get('available', False)
    if available and available != 'all':
        return jsonify({'materials': 'mistake in args'}), 400
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    DB_materials.id_material,
                    DB_materials.name,
                    DB_materials.width,
                    # DB_materials.thickness,
                    DB_materials.spool_qty,
                    DB_materials.spool_weight,
                    DB_materials.weight,
                    # DB_materials.manufacturer,
                    # DB_materials.reserve,
                    # DB_materials.weight_10m,
                    # DB_materials.comment
                )
                .order_by(DB_materials.id_material))
            if not available:
                stmt = stmt.where(DB_materials.weight != 0)
            materials = session.execute(stmt).fetchall()
            materials_data = []
            for material in materials:
                materials_data.append({
                    'id_material': material.id_material,
                    'name': material.name,
                    'spool_qty': material.spool_qty,
                    'width': material.width,
                    'net_weight': material.weight - (
                        material.spool_qty * material.spool_weight)})
        return jsonify(materials_data), 200
    except Exception as e:  # pragma: no cover
        logger.error({'materials_(GET)': e})
        return jsonify({'materials': e}), 400


@api.route('/materials/<int:id_material>', methods=['GET'])
@swag_from('/docs/get_material.yml')
def material_one_load(id_material: int) -> Dict:
    """read the material"""
    error_id_material = validate_id_material(id_material)
    if error_id_material:
        logger.error(f'{error_id_material}')
        return jsonify(error_id_material), 400
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    DB_materials.id_material,
                    DB_materials.name,
                    DB_materials.width,
                    DB_materials.thickness,
                    DB_materials.spool_qty,
                    DB_materials.spool_weight,
                    DB_materials.weight,
                    DB_materials.manufacturer,
                    DB_materials.reserve,
                    DB_materials.weight_10m,
                    DB_materials.comment)
                .where(DB_materials.id_material == id_material))
            material = session.execute(stmt).first()
            return jsonify({
                'comment': material.comment,
                'id_material': material.id_material,
                'manufacturer': material.manufacturer,
                'name': material.name,
                'reserve': material.reserve,
                'spool_qty': material.spool_qty,
                'spool_weight': material.spool_weight,
                'thickness': material.thickness,
                'weight': material.weight,
                'weight_10m': float(material.weight_10m) if material.weight_10m else 0,  # noqa
                'width': material.width}), 200
    except Exception as e:  # pragma: no cover
        logger.error({'materials_(GET)': e})
        return jsonify({'materials': e}), 400


@api.route('/materials/<int:id_material>', methods=['PUT'])
@swag_from('/docs/put_material.yml')
def edit_material(id_material) -> dict:
    """edit material"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/materials(POST) - format json is not correct')
        return jsonify({'materials': 'json format is not correct'}), 400

    error_id_material = validate_id_material(id_material)
    if error_id_material:
        logger.error(f'{error_id_material}')
        return jsonify(error_id_material), 400

    errors_validate = validate_material(data)
    if errors_validate:
        logger.error(f'{errors_validate}')
        return jsonify(errors_validate), 400

    try:
        with Session(engine) as session:
            stmt = (
                select(DB_materials.name)
                .where(DB_materials.id_material == id_material))
            if session.execute(stmt).first()[0] != data['name']:
                error_new_name = validate_new_name_material(data)
                if error_new_name:
                    logger.error(f'{error_new_name}')
                    return jsonify(error_new_name), 400

            stmt = (
                update(DB_materials)
                .where(DB_materials.id_material == id_material)
                .values(
                    id_material=id_material,
                    comment=data['comment'],
                    manufacturer=data['manufacturer'],
                    name=data['name'],
                    reserve=data['reserve'],
                    spool_qty=data['spool_qty'],
                    spool_weight=data['spool_weight'],
                    thickness=data['thickness'],
                    weight=data['weight'],
                    weight_10m=data['weight_10m'],
                    width=data['width']))
            session.execute(stmt)
            session.commit()
        return jsonify({'edit_material': id_material}), 202
    except Exception as e:  # pragma: no cover
        logger.error({'materials_(GET)': 'error in DB'})
        return jsonify({'materials': e}), 400


@api.route('/materials/consumption/<int:id_material>', methods=['PUT'])
@swag_from('/docs/put_material_consumption.yml')
def consumption_material(id_material) -> dict:
    """edit consumption material"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/materials(POST) - format json is not correct')
        return jsonify({'materials': 'json format is not correct'}), 400

    error_id_material = validate_id_material(id_material)
    if error_id_material:
        logger.error(f'{error_id_material}')
        return jsonify(error_id_material), 400

    errors_validate = errors_validate_consumption(data)
    if errors_validate:
        logger.error(f'{errors_validate}')
        return jsonify(errors_validate), 400

    try:
        with Session(engine) as session:
            stmt = (
                select(
                    DB_materials.weight,
                    DB_materials.spool_qty,
                    DB_materials.spool_weight)
                .where(DB_materials.id_material == id_material))
            material = session.execute(stmt).fetchone()
            spool_qty_result = material.spool_qty + data['edit_spool_qty']
            weight_result = material.weight + data['edit_weight']
            net_weight_result = weight_result - (
                spool_qty_result * material.spool_weight)

            stmt = (
                update(DB_materials)
                .where(DB_materials.id_material == id_material)
                .values(
                    spool_qty=spool_qty_result,
                    weight=weight_result))
            session.execute(stmt)
            session.commit()
        return jsonify({
            'spool_qty': spool_qty_result,
            'net_weight': net_weight_result,
            'weight': material.weight, }), 202
    except Exception as e:  # pragma: no cover
        logger.error({'consumption_material_(PUT)': 'error in DB'})
        return jsonify({'consumption_material': e}), 400
