"""Module for creating client"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.clients.models import DB_client
from app.clients.validator import (
    validate_client, validate_number, validate_id_client)

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


@api.route('/client/', methods=['POST'])
@swag_from('/docs/post_client.yml')
def create_client():
    """Creating new client"""
    try:
        data = request.get_json()
    except ValueError:
        logger.error('format json is not correct')
        return jsonify({'json': 'format is not correct'}), 400
    logger.info(f'Data for create new client: {data}')

    error_data = validate_client(data)
    if error_data:
        logger.error(f'{error_data}')
        return jsonify(error_data), 400
    
    error_number = validate_number(data)
    if error_number:
        logger.error(f'{error_number}')
        return jsonify(error_number), 400


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


@api.route('/client/<int:id_client>', methods=['GET'])
@swag_from('/docs/get_client.yml')
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


@api.route('/client/<int:id_client>', methods=['PUT'])
@swag_from('/docs/put_client.yml')
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
    