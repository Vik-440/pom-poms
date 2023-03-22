"""Module for creating client"""

from flask import request, jsonify
from sqlalchemy.orm import Session

from app.clients.models import DB_client
from app.clients.validator import validate_client

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/create_client/', methods=['POST'])
@swag_from('/docs/post_create_client.yml')
def create_client():
    """Creating new client"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    logger.info(f'Data for create new client: {data}')
    error = validate_client(data)
    if error:
        logger.error(f'{error}')
        return jsonify(error), 400

    with Session(engine) as session:
        stmt = DB_client(
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
            address=data['address'])
        session.add(stmt)
        session.commit()
        session.refresh(stmt)
        try:
            id_client = stmt.id_client
            return jsonify({"id_client": id_client}), 200
        except:
            logger.error('id_client: error in save order to DB')
            return  jsonify({"id_client": 'error in save order to DB'}), 400
