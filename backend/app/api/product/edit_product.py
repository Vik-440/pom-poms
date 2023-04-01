"""Module for edit product"""

from flask import request, jsonify
from sqlalchemy import update
from sqlalchemy.orm import Session 

from app.products.models import DB_product

from app.products.validator import (
    validate_product,
    validate_id_product,
    validate_article_product)

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/edit_product/<int:id_product>', methods=['PUT'])
@swag_from('/docs/put_edit_product.yml')
def edit_product(id_product):
    """Edit product"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    # logger.info(f'Data for create new product: {data}')
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
                    id_part_1=data['id_part_1'],
                    id_color_2=data['id_color_2'],
                    id_part_2=data['id_part_2'],
                    id_color_3=data['id_color_3'],
                    id_part_3=data['id_part_3'],
                    id_color_4=data['id_color_4'],
                    id_part_4=data['id_part_4'],
                    comment=data['comment']))
            session.execute(stmt)
            session.commit()
        return jsonify({"edit_product": id_product}), 200
    except:
        logger.error('id_product: error in save order to DB')
        return  jsonify({"id_product": 'error in save order to DB'}), 400
