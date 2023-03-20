"""Module for creating new order"""

# from datetime import datetime
from flask import request, jsonify
# from sqlalchemy import select #func, or_, and_, join, table
from sqlalchemy.orm import Session #, aliased
from sqlalchemy.sql.expression import func

from app.orders.models import DB_orders
# from app.clients.models import DB_client
# from app.products.models import DB_product
# from app.payments.models import DB_payment

from app.orders.validator import validate_create_order

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/create_order/', methods=['POST'])
@swag_from('/docs/post_create_order.yml')
def create_order():
    """Creating new order"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    logger.info(f'Data for create new order: {data}')
    errors_validate = validate_create_order(data)
    if errors_validate:
        logger.error(f'{errors_validate}')
        return jsonify(errors_validate), 400

    with Session(engine) as session:
        stmt = (func.max(DB_orders.id_order))
        id_order = session.execute(stmt).scalar() + 1
        stmt = DB_orders(
            id_order=id_order,
            date_create=data['date_create'],
            id_client=data['id_client'],
            id_recipient=data['id_recipient'],
            date_plane_send=data['date_plane_send'],
            discount=data['discount'],
            sum_payment=data['sum_payment'],
            status_order=data['status_order'],
            comment=data['comment'],
            phase_1=data['phase_1'],
            phase_2=data['phase_2'],
            phase_3=data['phase_3'],
            id_models=data['id_models'],
            qty_pars=data['qty_pars'],
            price_model_sell=data['price_model_sell'])
        session.add(stmt)
        session.commit()
        session.refresh(stmt)
        if id_order == stmt.id_order:
            return jsonify({"id_order": id_order}), 200
        else:
            logger.error('id_order: error in save order to DB')
            return  jsonify({"id_order": 'error in save order to DB'}), 400
