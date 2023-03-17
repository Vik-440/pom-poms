"""Module for changing phases of produce"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import update, select
from app.orders.models import DB_orders
from app import engine
from .. import api
from flasgger import swag_from


def validate_qty_phases(id_order: int, data: dict):
    with Session(engine) as session:
        stmt = (
            select(DB_orders.phase_1)
            .where(DB_orders.id_order == id_order))
        phases1_in_order = session.execute(stmt).scalar()
        qty_products_order = len(phases1_in_order)
        message = None
        if 'phase_1' in data:
            if len(data['phase_1']) != qty_products_order:
                message = {"message": "misstake in qty phases in data"}
        if 'phase_2' in data:
            if len(data['phase_2']) != qty_products_order:
                message = {"message": "misstake in qty phases in data"}
        if 'phase_3' in data:
            if len(data['phase_3']) != qty_products_order:
                message = {"message": "misstake in qty phases in data"}
    return message


@api.route('/main/phase/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_main_phase.yml')
def main_phase_get(id_order):
    """Module for changing phases in order"""
    with Session(engine) as session:
        data = request.get_json()
        if not data:
            return jsonify({"message": "misstake in data"}), 400
        message = validate_qty_phases(id_order, data)
        if message:
            return jsonify(message), 400

        phases = ['phase_1', 'phase_2', 'phase_3']
        for phase in phases:
            if phase in data:
                stmt = (
                    update(DB_orders)
                    .where(DB_orders.id_order == id_order)
                    .values(**{phase: data[phase]}))
                session.execute(stmt)
        session.commit()
        
    return {"message": "excellent"}, 200
