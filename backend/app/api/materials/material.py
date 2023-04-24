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


@api.route('/materials', methods=['GET'])
# @swag_from('/docs/post_material.yml')
# @swag_from('/docs/put_material.yml')
# @swag_from('/docs/get_material.yml') # /1
@swag_from('/docs/get_materials.yml') # + args all
# @swag_from('/docs/put_material_short.yml')
def materials():
    pass