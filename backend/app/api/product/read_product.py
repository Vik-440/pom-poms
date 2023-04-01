"""Module for read product"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.products.models import DB_product

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/read_product/<int:id_product>', methods=['GET'])
@swag_from('/docs/get_read_product.yml')
def read_product(id_product):
    """Read product"""

    # id_product = request.args.get('id_product')
    if id_product is None:
        return jsonify({'read_product': 'id_product is missing'}), 400

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
    