from flask import jsonify

from app.exceptions import ValidationError
from app.api import api


# def bad_request(message):
#     response = jsonify({'error': 'bad request', 'message': message})
#     response.status_code = 400
#     return response


# def unauthorized(message):
#     response = jsonify({'error': 'unauthorized', 'message': message})
#     response.status_code = 401
#     return response


# def forbidden(message):
#     response = jsonify({'error': 'forbidden', 'message': message})
#     response.status_code = 403
#     return response


# @api.errorhandler(ValidationError)
# def validation_error(error):
#     return bad_request(error.args[0])


class DatabaseError(Exception):
    pass
