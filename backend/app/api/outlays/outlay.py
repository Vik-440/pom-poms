"""module for outlay"""

from flask import jsonify, request
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, aliased
from werkzeug.exceptions import BadRequest

from app.outlay.models import DB_outlay
from app.outlay.validator import validate_outlay

from app import engine
from .. import api
from log.logger import logger


@api.route('/finance/outlay', methods=['POST'])
def creating_outlay():
    """module for create data in outlay"""
    try:
        data = request.get_json()
    except BadRequest:
        logger.error('/outlay(POST) - format json is not correct')
        return jsonify({'outlay(POST)': 'json format is not correct'}), 400
    error_outlay = validate_outlay(data)
    if error_outlay:
        logger.error(f'{error_outlay}')
        return jsonify(error_outlay), 400
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
        return jsonify({'message': 'creating_outlay is excellent'}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function finance: {e}') # pragma: no cover
        return f'Error in function finance: {e}', 400 # pragma: no cover


@api.route('/finance/outlay/<int:id_outlay>', methods=['PUT'])
def edit_outlay(id_outlay):
    try:
        data = request.get_json()
    except BadRequest:
        logger.error('/outlay(PUT) - format json is not correct')
        return jsonify({'outlay(PUT)': 'json format is not correct'}), 400
    error_outlay = validate_outlay(data)
    if error_outlay:
        logger.error(f'{error_outlay}')
        return jsonify(error_outlay), 400
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
        return jsonify({'message': 'outlay_changing excellent'}), 200
    except Exception as e: # pragma: no cover
        logger.error(f'Error in function finance: {e}') # pragma: no cover
        return f'Error in function finance: {e}', 400 # pragma: no cover


@api.route('/finance/outlays', methods=['GET'])
def opening_last_outlays():
    """return last N outlays"""
    try:
        with Session(engine) as session:
            stmt = (
                select(
                    DB_outlay.id_outlay,
                    DB_outlay.data_outlay,
                    DB_outlay.id_outlay_class,
                    DB_outlay.money_outlay,
                    DB_outlay.comment)
                .order_by(DB_outlay.id_outlay.desc())
                .limit(5))
            outlays = session.execute(stmt).all()
            full_block = []
            for row in outlays:
                one_block = {"id_outlay": row.id_outlay,
                             "data_outlay": str(row.data_outlay),
                             "id_outlay_class": row.id_outlay_class,
                             "money_outlay": row.money_outlay,
                             "comment_outlay": row.comment}
                full_block.insert(0, one_block)
        return jsonify(full_block)
    except Exception as e: # pragma: no cover
        logger.error(f'Error in finance_outlays GET: {e}') # pragma: no cover
        return f'Error in finance_outlays GET: {e}', 400 # pragma: no cover