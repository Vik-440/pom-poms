"""Module for creating new order"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import update, select #func, or_, and_, join, table
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql.expression import func

from app.orders.models import DB_orders
from app.clients.models import DB_client
from app.products.models import DB_product
from app.payments.models import DB_payment

from app.orders.validator import validate_create_order, validate_id_order

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/edit_order/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_edit_order.yml')
def edit_order(id_order):
    """Edit order"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    logger.info(f'Data for create new order: {id_order, data}')
    validate_id_order_number = validate_id_order(id_order)
    if validate_id_order_number:
        logger.error(f'error: {validate_id_order_number}')
        return jsonify(validate_id_order_number), 400

    validate_data = validate_create_order(data)
    if validate_data:
        logger.error(f'error: {validate_data}')
        return jsonify(validate_data), 400
    try:
        with Session(engine) as session:
            stmt = (
                update(DB_orders)
                .where(DB_orders.id_order == id_order)
                .values(
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
                    price_model_sell=data['price_model_sell']))
            session.execute(stmt)
            session.commit()
        return jsonify({"edit_order": id_order}), 200
    except:
        logger.error(f'edit_order {id_order} error')
        return jsonify({"edit_order": id_order}), 400
