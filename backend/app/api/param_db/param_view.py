"""Rout for CRUD parameters saved in DB"""

from flask import request, jsonify
from sqlalchemy import select, delete, update  # func
from sqlalchemy.orm import Session
from typing import Dict
from werkzeug.exceptions import BadRequest
from flasgger import swag_from

from app.param_db.models import ParamDb
from app.param_db.serializers import (
    param_serializer,
    param_check_name,
)
from app import engine
from .. import api


@api.route('/param', methods=['POST'])
@swag_from('/docs/post_param_db.yml')
def parameter_db_post() -> dict:
    """POST Route for param"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        return jsonify({'param': 'json format is not correct'}), 400

    error_validate = param_serializer(data)
    if error_validate:
        return jsonify(error_validate), 400
    error_name = param_check_name(data)
    if error_name:
        return jsonify(error_name), 400

    try:
        with Session(engine) as session:
            stmt = ParamDb(
                parameter_name=data['parameter_name'],
                parameter_str=data['parameter_str'],
                parameter_int=data['parameter_int'],
                parameter_description=data['parameter_description']
            )
            session.add(stmt)
            session.commit()
            return jsonify({'param_created': 'OK'}), 201
    except Exception as e:
        return jsonify({'param_created': e}), 400


@api.route('/param/<string:params_names>', methods=['GET'])
@swag_from('/docs/get_param_path_db.yml')
def parameter_db_get(params_names: str) -> Dict:
    """read data from DB by query"""
    keys_list = params_names.split(',')
    if len(keys_list) == 0:
        return jsonify({'param': 'query is empty'})
    with Session(engine) as session:
        stmt = (
            select(
                ParamDb.parameter_name,
                ParamDb.parameter_str,
                ParamDb.parameter_int,
                ParamDb.parameter_description,
            )
            .order_by(ParamDb.parameter_name)
        )
        params = session.execute(stmt).fetchall()
        params_list = []
        for param in params:
            params_list.append({
                param.parameter_name: {
                    'parameter_str': param.parameter_str,
                    'parameter_int': param.parameter_int,
                    'parameter_description': param.parameter_description,
                }}
            )
        parameters_answer = {}
        for item in params_list:
            if list(item.keys())[0] in keys_list:
                parameters_answer.update(item)
        for key in keys_list:
            if key not in list(parameters_answer.keys()):
                parameters_answer.update({key: 'not existed'})
        return jsonify(parameters_answer)


@api.route('/param', methods=['GET'])
@swag_from('/docs/get_param_db.yml')
def parameter_db_get_all() -> Dict:
    """read data from DB by query"""
    with Session(engine) as session:
        stmt = (
            select(
                ParamDb.parameter_name,
            )
            .order_by(ParamDb.parameter_name)
        )
        params = session.execute(stmt).fetchall()
        params_list = [row[0] for row in params]
        return jsonify(params_list)


@api.route('/param/<string:params_name>', methods=['DELETE'])
@swag_from('/docs/del_param_db.yml')
def parameter_db_delete(params_name) -> Dict:
    """delete parameter from DB by query"""

    with Session(engine) as session:
        try:
            stmt = (
                delete(ParamDb)
                .where(ParamDb.parameter_name == params_name)
            )
            session.execute(stmt)
            session.commit()
            return jsonify({'param_deleted': 'OK'}), 204
        except Exception as e:
            session.rollback()
            return {'param_deleted': 'error', 'message': str(e)}, 400


@api.route('/param/<string:params_name>', methods=['PATCH'])
@swag_from('/docs/patch_param_db.yml')
def parameter_db_patch(params_name) -> Dict:
    """patch parameter from DB by query"""
    try:
        data = request.get_json(force=True)
    except BadRequest:
        return jsonify({'param': 'json format is not correct'}), 400
    error_validate = param_serializer(data)
    if error_validate:
        return jsonify(error_validate), 400

    with Session(engine) as session:
        try:
            stmt = (
                    select(ParamDb.parameter_name)
                    .where(ParamDb.parameter_name == params_name)
                )
            res = session.execute(stmt).first()
            if res is None:
                return {params_name: 'is not existed'}

            stmt = (
                update(ParamDb)
                .where(ParamDb.parameter_name == params_name)
                .values(
                    parameter_str=data.get('parameter_str', None),
                    parameter_int=data.get('parameter_int', 0),
                    parameter_description=data.get(
                        'parameter_description', None),
                )
            )
            session.execute(stmt)
            session.commit()
            return jsonify({'params_updated': 'OK'}), 202
        except Exception as e:
            session.rollback()
            return {'params_patch': 'error', 'message': str(e)}, 400
