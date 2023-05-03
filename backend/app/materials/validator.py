from sqlalchemy import select
from sqlalchemy.orm import Session

from app.materials.models import DB_materials
from utils.validators import validate_field
from app import engine


def validate_id_material(id_material: int):
    """Validator for ID material"""
    with Session(engine) as session:
        stmt = (
            select(DB_materials.id_material)
            .where(DB_materials.id_material == id_material))
        if not session.execute(stmt).first():
            return {'id_material': f'ID product {id_material} is invalid'}
    return


def validate_new_name_material(data: dict):
    """Validator for name material"""
    with Session(engine) as session:
        stmt = (
            select(DB_materials.name)
            .where(DB_materials.name == data['name']))
        if session.execute(stmt).first():
            return {'name': f'name {data["name"]} already exists'}
    return


def validate_material(data: dict):
    """validate create or edit material"""
    fields_to_check = [
        ('comment', (str, type(None))),
        ('manufacturer', str),
        ('name', str),
        ('reserve', int),
        ('spool_qty', int),
        ('spool_weight', int),
        ('thickness', int),
        ('weight', int),
        ('weight_10m', (int, float)),
        ('width', int)]
    for field, field_type in fields_to_check:
        error = validate_field(field, field_type, data)
        if error:
            return error
    data['weight_10m'] = round(data['weight_10m'], 2)
    return


def errors_validate_consumption(data: dict):
    """validate consumption material"""
    for field, field_type in [
            ('edit_spool_qty', (int, type(None))),
            ('edit_weight', (int, type(None))),]:
        error = validate_field(field, field_type, data)
        if error:
            return error
        if data[field] is None:
            data[field] = 0
    return
