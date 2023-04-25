"""Module for extract id_material about materials"""

# from datetime import datetime
from flask import request, jsonify
from sqlalchemy import select, update#, func, or_, and_, join, table
from sqlalchemy.orm import Session#, aliased

from app.materials.models import DB_materials
# from app.materials.forms import MaterialForm
from app import engine
from .. import api
from log.logger import logger
from flasgger import swag_from


@api.route('/materials', methods=['POST'])
@swag_from('/docs/post_material.yml')
def create_material() -> dict:
    """create material"""
    return jsonify({'create_material': 'test OK'}), 201


@api.route('/materials', methods=['GET'])
@swag_from('/docs/get_materials.yml')
def materials() -> dict:
    """read materials in general"""
    return jsonify({'materials': 'test OK'}), 200


@api.route('/materials/<int:id_material>', methods=['GET'])
@swag_from('/docs/get_material.yml')
def material_one_load(id_material: int) -> dict:
    """read the material"""
    return jsonify({'material': 'test OK'}), 200


@api.route('/materials/<int:id_material>', methods=['PUT'])
@swag_from('/docs/put_material.yml')
def edit_material(id_material) -> dict:
    """edit material"""
    return jsonify({'edit_material': 'test OK'}), 202


@api.route('/materials/consumption/<int:id_material>', methods=['PUT'])
@swag_from('/docs/put_material_consumption.yml')
def consumption_material(id_material) -> dict:
    """edit material"""
    return jsonify({'consumption_material': 'test OK'}), 202