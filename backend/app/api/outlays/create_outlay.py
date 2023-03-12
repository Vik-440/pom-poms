"""module for create data in outlay"""

from flask import jsonify, request
from sqlalchemy.orm import Session, aliased

from app.outlay.models import DB_outlay
from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/outlay', methods=['POST'])
def creating_outlay():
    """module for create data in outlay"""
    data = request.get_json()
    try:
        with Session(engine) as session:
            stmt = (
                DB_outlay(
                    data_outlay=data['data_outlay'],
                    id_outlay_class=data['id_outlay_class'],
                    money_outlay=data['money_outlay'],
                    comment=data['comment_outlay']))
            session.add(stmt)
            session.commit()
        return jsonify({"message": "creating_outlay is excellent"}), 200
    except Exception as e:
        logger.error(f'Error in function finance: {e}')
        return f'Error in function finance: {e}', 500
    