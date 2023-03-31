"""Module for creating product"""

from flask import request, jsonify
from sqlalchemy.orm import Session 

from app.products.models import DB_product

from app.products.validator import validate_product

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/create_product', methods=['POST'])
@swag_from('/docs/post_create_product.yml')
def create_product():
    """Creating new product"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    error = validate_product(data)
    if error:
        logger.error(f'{error}')
        return jsonify(error), 400

    # print(data)
    with Session(engine) as session:
        stmt = DB_product(
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
            comment=data['comment'])
        session.add(stmt)
        session.commit()
        session.refresh(stmt)
        try:
            id_product = stmt.id_product
            return jsonify({"id_product": id_product}), 200
        except:
            logger.error('id_product: error in save order to DB')
            return  jsonify({"id_product": 'error in save order to DB'}), 400
