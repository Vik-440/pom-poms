"""Module for creating product"""

from flask import request, jsonify
from sqlalchemy.orm import Session, aliased
from sqlalchemy import update, select
from werkzeug.exceptions import BadRequest

from app.products.models import DB_product
from app.materials.models import DB_materials
from app.api.errors import DatabaseError

from app.products.validator import (
    validate_product,
    validate_article_product,
    validate_id_product)

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/product', methods=['POST'])
@swag_from('/docs/post_product.yml')
def create_product():
    """Creating new product"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/product(POST) - format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    error_article = validate_article_product(data)
    if error_article:
        logger.error(f'{error_article}')
        return jsonify(error_article), 400
    error_product = validate_product(data)
    if error_product:
        logger.error(f'{error_product}')
        return jsonify(error_product), 400

    try:
        with Session(engine) as session:
            stmt = DB_product(
                article=data['article'],
                colors=data['colors'],
                price=data['price'],
                id_color_1=data['id_color_1'],
                part_1=data['part_1'],
                id_color_2=data['id_color_2'],
                part_2=data['part_2'],
                id_color_3=data['id_color_3'],
                part_3=data['part_3'],
                id_color_4=data['id_color_4'],
                part_4=data['part_4'],
                comment=data['comment'])
            session.add(stmt)
            session.commit()
            session.refresh(stmt)
            id_product = stmt.id_product
            return jsonify({"id_product": id_product}), 200
    except DatabaseError:
        logger.error('id_product: error in save order to DB')
        return  jsonify({"id_product": 'error in save order to DB'}), 400


@api.route('/product/<int:id_product>', methods=['GET'])
@swag_from('/docs/get_product.yml')
def read_product(id_product):
    """Read product"""
    error_id = validate_id_product(id_product)
    if error_id:
        logger.error(f'{error_id}')
        return jsonify(error_id), 400
    with Session(engine) as session:
        color_name_1 = aliased(DB_materials)
        color_name_2 = aliased(DB_materials)
        color_name_3 = aliased(DB_materials)
        color_name_4 = aliased(DB_materials)
        stmt = (
            select(
                DB_product.id_product,
                DB_product.article,
                DB_product.colors,
                DB_product.price,
                DB_product.comment,
                DB_product.id_color_1,
                DB_product.id_color_2,
                DB_product.id_color_3,
                DB_product.id_color_4,
                DB_product.part_1,
                DB_product.part_2,
                DB_product.part_3,
                DB_product.part_4,
                color_name_1.name.label('color_name_1'),
                color_name_2.name.label('color_name_2'),
                color_name_3.name.label('color_name_3'),
                color_name_4.name.label('color_name_4')
                )
            .group_by(DB_product, color_name_1, color_name_2, color_name_3, color_name_4)
            .join(color_name_1, DB_product.id_color_1 == color_name_1.id_material)
            .join(color_name_2, DB_product.id_color_2 == color_name_2.id_material, isouter=True)
            .join(color_name_3, DB_product.id_color_3 == color_name_3.id_material, isouter=True)
            .join(color_name_4, DB_product.id_color_4 == color_name_4.id_material, isouter=True)
            .where(DB_product.id_product == id_product))
        product = session.execute(stmt).first()
        if product:
            return jsonify({
                'id_product': product.id_product,
                'article': product.article,
                'colors': product.colors,
                'price': product.price,
                'id_color_1': product.id_color_1,
                'part_1': product.part_1,
                'id_color_2': product.id_color_2,
                'part_2': product.part_2,
                'id_color_3': product.id_color_3,
                'part_3': product.part_3,
                'id_color_4': product.id_color_4,
                'part_4': product.part_4,
                'comment': product.comment,
                'color_name_1': product.color_name_1,
                'color_name_2': product.color_name_2,
                'color_name_3': product.color_name_3,
                'color_name_4': product.color_name_4
            }), 200
        return jsonify({"read_product": 'ID product is not exist'}), 400


@api.route('/product/<int:id_product>', methods=['PUT'])
@swag_from('/docs/put_product.yml')
def edit_product(id_product):
    """Edit product"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/product(PUT) - format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    error_id = validate_id_product(id_product)
    if error_id:
        logger.error(f'{error_id}')
        return jsonify(error_id), 400
    error_product = validate_product(data)
    if error_product:
        logger.error(f'{error_product}')
        return jsonify(error_product), 400

    try:
        with Session(engine) as session:
            stmt = (
                update(DB_product)
                .where(DB_product.id_product == id_product)
                .values(
                    article=data['article'],
                    colors=data['colors'],
                    price=data['price'],
                    id_color_1=data['id_color_1'],
                    part_1=data['part_1'],
                    id_color_2=data['id_color_2'],
                    part_2=data['part_2'],
                    id_color_3=data['id_color_3'],
                    part_3=data['part_3'],
                    id_color_4=data['id_color_4'],
                    part_4=data['part_4'],
                    comment=data['comment']))
            session.execute(stmt)
            session.commit()
        return jsonify({"edit_product": id_product}), 200
    except:
        logger.error('id_product: error in save order to DB')
        return  jsonify({"id_product": 'error in save order to DB'}), 400
