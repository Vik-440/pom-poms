"""Serializers for parameters saved in DB"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.param_db.models import ParamDb
# from utils.validators import validate_field
from app import engine


def param_serializer(data: dict):
    """Serializer for parameters data"""
    fields = {
        'parameter_name': str,
        'parameter_str': str,
        'parameter_int': int,
        'parameter_description': str,
    }
    try:
        for key, value in fields.items():
            if key in data:
                if not isinstance(data[key], value):
                    return {'param': f'param {key} is not {value}'}
    except Exception as e:
        return {'param': e}
    return


def param_check_name(data: dict):
    """Check on unique name in params"""
    try:
        with Session(engine) as session:
            stmt = (
                select(ParamDb.parameter_name)
                .where(ParamDb.parameter_name == data['parameter_name'])
            )
            res = session.execute(stmt).first()
            if res is not None:
                return {data['parameter_name']: 'is existed'}
            return
    except Exception as e:
        return e
