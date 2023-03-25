"""Module for read order"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.orders.models import DB_orders

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/read_order/<int:id_order>', methods=['GET'])
@swag_from('/docs/get_read_order.yml')
def read_order(id_order):
    """Read order"""

    logger.info(f'Read order: {id_order}')

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
    