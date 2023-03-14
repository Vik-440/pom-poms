"""module for edit data in outlay"""

from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.outlay.models import DB_outlay
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/outlay/<int:id_outlay>', methods=['PUT'])
def edit_outlay(id_outlay):
    data = request.get_json()
    try:
        with Session(engine)as session:
            stmt = (
                update(DB_outlay)
                .where(DB_outlay.id_outlay == id_outlay)
                .values(
                    data_outlay=data['data_outlay'],
                    id_outlay_class=data['id_outlay_class'],
                    money_outlay=data['money_outlay'],
                    comment=data['comment_outlay']))
            session.execute(stmt)
            session.commit()
        return jsonify({"message": "outlay_changing excellent"}), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500
    