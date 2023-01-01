from flask import request
from app import app

from functions.orders.new_order_json import (
    return_data_from_new_order,
    return_data_from_new_order_post)
from log.logger import logger


@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            data = return_data_from_new_order_post(request.data)
            return data, 200
        else:
            return (return_data_from_new_order())
    except Exception as e:
        logger.error(f'Error in function new_order: {e}')
        return f'Error in function new_order: {e}', 500
