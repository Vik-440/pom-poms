"""Module for creating product"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import update, select

from app.products.models import DB_product

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
    # try:
    data = request.get_json()
    # except ValueError:
    #     logger.error('format json is not correct')
    #     return jsonify({'json': 'format is not correct'}), 400
    error_article = validate_article_product(data)
    if error_article:
        logger.error(f'{error_article}')
        return jsonify(error_article), 400
    error_product = validate_product(data)
    if error_product:
        logger.error(f'{error_product}')
        return jsonify(error_product), 400

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
        # try:
        id_product = stmt.id_product
        return jsonify({"id_product": id_product}), 200
        # except:
        #     logger.error('id_product: error in save order to DB')
        #     return  jsonify({"id_product": 'error in save order to DB'}), 400


@api.route('/product/<int:id_product>', methods=['GET'])
@swag_from('/docs/get_product.yml')
def read_product(id_product):
    """Read product"""

    # if id_product is None:
    #     return jsonify({'read_product': 'id_product is missing'}), 400
    with Session(engine) as session:
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
                DB_product.id_part_1,
                DB_product.id_part_2,
                DB_product.id_part_3,
                DB_product.id_part_4)
            .where(DB_product.id_product == id_product))
        product = session.execute(stmt).first()
        if product:
            return jsonify({
                'id_product': product.id_product,
                'article': product.article,
                'colors': product.colors,
                'price': product.price,
                'id_color_1': product.id_color_1,
                'id_part_1': product.id_part_1,
                'id_color_2': product.id_color_2,
                'id_part_2': product.id_part_2,
                'id_color_3': product.id_color_3,
                'id_part_3': product.id_part_3,
                'id_color_4': product.id_color_4,
                'id_part_4': product.id_part_4,
                'comment': product.comment
            }), 200
        return jsonify({"read_product": 'ID product is not exist'}), 400


@api.route('/product/<int:id_product>', methods=['PUT'])
@swag_from('/docs/put_product.yml')
def edit_product(id_product):
    """Edit product"""
    # try:
    data = request.get_json()
    # except ValueError:
    #     logger.error('format json is not correct')
    #     return jsonify({'json': 'format is not correct'}), 400
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
