from flask import request
from app import app

from functions.materials.material_json import (
    return_data_from_material,
    return_data_from_material_one,
    return_data_from_material_change,
    return_data_from_material_new,
    return_data_from_material_change_full)
from log.logger import logger


@app.route('/material', methods=['GET', 'POST'])
def material():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            if 'id_color' in request.data:
                tmp_id_color = request.data['id_color']
                if tmp_id_color == 999:
                    data = return_data_from_material(999)
                else:
                    data = return_data_from_material_one(request.data)
            elif 'color_new' in request.data:
                data = return_data_from_material_new(request.data)
            elif 'color_change' in request.data:
                data = return_data_from_material_change(request.data)
            elif 'color_change_full' in request.data:
                data = return_data_from_material_change_full(request.data)
            else:
                data = {"запит ": "не вірний"}
            return data, 200
        else:
            return (return_data_from_material(0)), 200
    except Exception as e:
        logger.error(f'Error in function material: {e}')
        return f'Error in function material: {e}', 500
