from flask import request
from app import app

from functions.materials.material_base_table import (
    extracting_material_all,
    extracting_material_one)
from functions.materials.material_create_new import (
    material_creating_new)
from functions.materials.material_change_data import (
    changing_material_one,
    changing_material_full)
from log.logger import logger


@app.route('/material', methods=['GET'])
def material():
    try:
        return (extracting_material_all(0)), 200
    except Exception as e:
        logger.error(f'Error in function material GET: {e}')
        return f'Error in function material GET: {e}', 500


@app.route('/material', methods=['POST'])
def material_post():
    try:
        request.data = request.get_json()
        if 'id_color' in request.data:
            id_color = request.data['id_color']
            if id_color == 999:
                data = extracting_material_all(999)
            else:
                data = extracting_material_one(request.data)
        elif 'color_new' in request.data:
            data = material_creating_new(request.data)
        elif 'color_change' in request.data:
            data = changing_material_one(request.data)
        elif 'color_change_full' in request.data:
            data = changing_material_full(request.data)
        else:
            data = {"запит ": "не вірний"}
        return data, 200
    except Exception as e:
        logger.error(f'Error in function material POST: {e}')
        return f'Error in function material POST: {e}', 500
