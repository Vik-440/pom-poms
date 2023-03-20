"""Module for changing status order"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.orders.models import DB_orders
from app import engine
from .. import api

from flasgger import Swagger, swag_from


@api.route('/main/status/<int:id_order>', methods=['PUT'])
@swag_from('/docs/put_main_status.yml')
def main_status_order(id_order):
    """Module for changing status in produce process"""
    if not 'status_order' in request.get_json():
        return {"error": "misstake in data status"}, 400
    status_order = request.get_json()['status_order']
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
