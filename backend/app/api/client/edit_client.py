"""Edit client"""

from flask import request, jsonify
from sqlalchemy import update
from sqlalchemy.orm import Session #, aliased
from sqlalchemy.sql.expression import func

from app.clients.models import DB_client

from app.clients.validator import validate_client, validate_id_client

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/edit_client/<int:id_client>', methods=['PUT'])
@swag_from('/docs/put_edit_client.yml')
def edit_client(id_client: int):
    """Edit client"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    logger.info(f'Data for create new client: {data}')
    error = validate_id_client(id_client)
    if error:
        logger.error(f'{error}')
        return jsonify(error), 400
    error = validate_client(data)
    if error:
        logger.error(f'{error}')
        return jsonify(error), 400
    try:
        with Session(engine) as session:
            stmt = (
                update(DB_client)
                .where(DB_client.id_client == id_client)
                .values(
                    id_client=id_client,
                    phone=data['phone'],
                    second_name=data['second_name'],
                    first_name=data['first_name'],
                    surname=data['surname'],
                    city=data['city'],
                    np_number=data['np_number'],
                    comment=data['comment'],
                    team=data['team'],
                    coach=data['coach'],
                    zip_code=data['zip_code'],
                    address=data['address']))
            session.execute(stmt)
            session.commit()
        return jsonify({"edit_client": id_client}), 200
    except:
        logger.error('id_client: error in save order to DB')
        return  jsonify({"id_client": 'error in save order to DB'}), 400
