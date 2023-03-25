"""Module for read client"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.clients.models import DB_client

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/read_client/<int:id_client>', methods=['GET'])
@swag_from('/docs/get_read_client.yml')
def read_client(id_client):
    """Read client"""

    logger.info(f'Read client: {id_client}')

    with Session(engine) as session:
        stmt = (
            select(
                DB_client.id_client,
                DB_client.phone,
                DB_client.second_name,
                DB_client.first_name,
                DB_client.surname,
                DB_client.city,
                DB_client.np_number,
                DB_client.comment,
                DB_client.team,
                DB_client.coach,
                DB_client.zip_code,
                DB_client.address)
            .where(DB_client.id_client == id_client))
        client = session.execute(stmt).first()
        if client:
            return jsonify({
                'id_client': client.id_client,
                'phone': client.phone,
                'second_name': client.second_name,
                'first_name': client.first_name,
                'surname': client.surname,
                'city': client.city,
                'np_number': client.np_number,
                'team': client.team,
                'coach': client.coach,
                'zip_code': client.zip_code,
                'address': client.address,
                'comment': client.comment
            }), 200
        return jsonify({"read_client": 'ID client is not exist'}), 400
    