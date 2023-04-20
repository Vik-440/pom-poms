"""Module for changing status order"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.orders.models import DB_orders
from app.orders.validator import validate_id_order, validate_status
from werkzeug.exceptions import BadRequest
from app import engine
from .. import api

from flasgger import Swagger, swag_from
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
                pre_data = session.execute(stmt).first()
                phaze_to_ziro = []
                for step in pre_data:
                    for _ in step:
                        phaze_to_ziro.append(0)
                stmt = (
                    update(DB_orders)
                    .where(DB_orders.id_order == id_order)
                    .values(
                        status_order=True,
                        phase_1=phaze_to_ziro,
                        phase_2=phaze_to_ziro,
                        phase_3=phaze_to_ziro,
                        date_plane_send=today))
            session.execute(stmt)
            session.commit()
        return jsonify({"message": "excellent"}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in put_main_status: {e}') # pragma: no cover
        return f'Error in put_main_status: {e}', 400 # pragma: no cover