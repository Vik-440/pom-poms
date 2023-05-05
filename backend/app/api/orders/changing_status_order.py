"""Module for changing status order"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from app.orders.models import DB_orders
from app.orders.validator import validate_id_order, validate_status
from app import engine
from .. import api

from flasgger import swag_from
from log.logger import logger


@api.route('/main/status/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_main_status.yml')
def main_status_order(id_order):
    """Module for changing status in produce process"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('/status(PUT) - format json is not correct')
        return jsonify({'status(PUT)': 'json format is not correct'}), 400
    
    error_id_order = validate_id_order(id_order)
    if error_id_order:
        logger.error(f'{error_id_order}')
        return jsonify(error_id_order), 400
    
    error_status_data = validate_status(data)
    if error_status_data:
        logger.error(f'{error_status_data}')
        return jsonify(error_status_data), 400
    
    status_order = data['status_order']
    try:
        with Session(engine) as session:
            if not status_order:
                stmt = update(DB_orders).where(
                    DB_orders.id_order == id_order).values(status_order=False)
            else:
                today = datetime.today().strftime('%Y-%m-%d')
                stmt = (
                    select(DB_orders.qty_pars)
                    .where(DB_orders.id_order == id_order))
                
                phase_to_zero = [0 for _ in range(len(session.execute(stmt).first()))]

                stmt = (
                    update(DB_orders)
                    .where(DB_orders.id_order == id_order)
                    .values(
                        status_order=True,
                        phase_1=phase_to_zero,
                        phase_2=phase_to_zero,
                        phase_3=phase_to_zero,
                        date_plane_send=today))
            session.execute(stmt)
            session.commit()
        return jsonify({'message': 'excellent'}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in put_main_status: {e}')
        return f'Error in put_main_status: {e}', 400