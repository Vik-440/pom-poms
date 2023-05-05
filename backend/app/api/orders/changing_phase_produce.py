"""Module for changing phases of produce"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.orders.models import DB_orders
from app.orders.validator import validate_id_order, validate_phases
from werkzeug.exceptions import BadRequest
from app import engine
from .. import api
from flasgger import swag_from
from log.logger import logger


@api.route('/main/phase/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_main_phase.yml')
def change_main_phase(id_order):
    """Module for changing phases in order"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        logger.error('phases(PUT) - format json is not correct')
        return jsonify({'phases(PUT)': 'json format is not correct'}), 400
    
    error_id_order = validate_id_order(id_order)
    if error_id_order:
        logger.error(f'{error_id_order}')
        return jsonify(error_id_order), 400
    
    error_phases_data = validate_phases(id_order, data)
    if error_phases_data:
        logger.error(f'{error_phases_data}')
        return jsonify(error_phases_data), 400
    
    try:
        with Session(engine) as session:
            phases = ['phase_1', 'phase_2', 'phase_3']
            for phase in phases:
                if phase in data:
                    stmt = (
                        update(DB_orders)
                        .where(DB_orders.id_order == id_order)
                        .values(**{phase: data[phase]}))
                    session.execute(stmt)
            session.commit()
        return jsonify({"message": "excellent"}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in put_main_phases: {e}')
        return f'Error in put_main_phases: {e}', 400
