"""Module for extract last outlays for finance page"""

from datetime import datetime
from flask import jsonify
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.outlay.models import DB_outlay
from app import engine
from .. import api
from log.logger import logger


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
    except Exception as e:
        logger.error(f'Error in finance_outlays GET: {e}')
        return f'Error in finance_outlays GET: {e}', 500
    