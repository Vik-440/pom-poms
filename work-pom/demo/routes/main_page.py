from flask import request
from app import app

from functions.main_page.get_main_search import get_main
from functions.main_page.changing_phase_produce import changing_order_phases
from functions.main_page.changing_status_order import changing_status_order

from functions.main_page_json import return_data_from_main_page
from functions.main_page_json import change_main_phase
from log.logger import logger


@app.route('/main', methods=['GET'])
def main():
    """Preparing main page with or without same requests"""
    try:
        if request.method == 'GET':
            data = request.args
            logger.info('Get main is work!')
            return (get_main(data))
        else:
            return ({"request_metod": "error"}), 500
    except Exception as e:
        logger.error(f'Error in function main: {e}')
        return f'Error in function main: {e}', 500


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    """Old route, which must be deleting in finish"""
    try:
        if request.method == 'POST':
            request.data = request.get_json()
            return (return_data_from_main_page(request.data))
        # ds=datetime.today().strftime('%Y-%m-%d')
        elif request.method == 'GET':
            data = {"data_start": "2016-01-01"}
            logger.info('Get main_page is work!')
            return (return_data_from_main_page(data))
        else:
            return ({"request_metod": "error"}), 500
    except Exception as e:
        logger.error(f'Error in function mainpage: {e}')
        return f'Error in function mainpage: {e}', 500


@app.route('/main_page/phase/<int:id>', methods=['PUT'])
def main_phase(id):
    """Old route, which must be deleting in finish"""
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (change_main_phase(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function main_phase: {e}')
        return f'Error in function main_phase: {e}', 500


@app.route('/main/phase/<int:id>', methods=['PUT'])
def main_phase_get(id):
    """Module for changing phases in produce process"""
    request.data = request.get_json()
    try:
        if request.method == 'PUT':
            return (changing_order_phases(id, request.data)), 200
        else:
            return ({"error_message": "mistake method"}), 404
    except Exception as e:
        logger.error(f'Error in function main_phase: {e}')
        return f'Error in function main_phase: {e}', 500


@app.route('/main/status/<int:id>', methods=['PUT'])
def main_status_order(id):
    """Module for changing status in produce process"""
    request.data = request.get_json()
    try:
        return (changing_status_order(id, request.data)), 200
    except Exception as e:
        return f'Error in function main_status_order: {e}', 500
