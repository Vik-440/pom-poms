"""Module for changing phases of produce"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.orders.models import DB_orders
from app import engine
from .. import api


@api.route('/main/phase/<int:id_order>', methods=['PUT'])
def main_phase_get(id_order):
    """Module for changing phases in order"""
    with Session(engine) as session:
        data = request.get_json()
        if not data:
            return {"message": "misstake in data"}, 400
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
