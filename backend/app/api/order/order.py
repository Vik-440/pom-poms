"""Module for creating new order"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import update, select

from app.orders.models import DB_orders

from app.orders.validator import (
    validate_create_order, validate_id_order)

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/order/', methods=['POST'])
@swag_from('/docs/post_order.yml')
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


@api.route('/order/<int:id_order>', methods=['GET'])
@swag_from('/docs/get_order.yml')
def read_order(id_order):
    """Read order"""

    with Session(engine) as session:
        stmt = (
            select(
                DB_orders.id_order,
                DB_orders.date_create,
                DB_orders.date_plane_send,
                DB_orders.id_client,
                DB_orders.comment,
                DB_orders.id_recipient,
                DB_orders.status_order,
                DB_orders.sum_payment,
                DB_orders.discount,
                DB_orders.id_models,
                DB_orders.qty_pars,
                DB_orders.price_model_sell,
                DB_orders.phase_1,
                DB_orders.phase_2,
                DB_orders.phase_3)
            .where(DB_orders.id_order == id_order))
        order = session.execute(stmt).first()
        if order:
            return jsonify({
                'id_order': order.id_order,
                'date_create': order.date_create,
                'date_plane_send': order.date_plane_send,
                'id_client': order.id_client,
                'id_recipient': order.id_recipient,
                'status_order': order.status_order,
                'sum_payment': order.sum_payment,
                'discont': order.discount,
                'comment': order.comment,
                'id_models': order.id_models,
                'qty_pars': order.qty_pars,
                'price_model_sell': order.price_model_sell,
                'phase_1': order.phase_1,
                'phase_2': order.phase_2,
                'phase_3': order.phase_3
            }), 200
        return jsonify({"read_order": 'ID order is not exist'}), 400


@api.route('/order/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_order.yml')
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
        logger.error(f'{validate_id_order_number}')
        return jsonify(validate_id_order_number), 400

    validate_data = validate_create_order(data)
    if validate_data:
        logger.error(f'{validate_data}')
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
