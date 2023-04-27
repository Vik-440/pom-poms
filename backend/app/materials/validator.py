from sqlalchemy import select
from sqlalchemy.orm import Session

from app.materials.models import DB_materials
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
    """Validate data for create or edit material"""
    if not 'comment' in data:
        return {'comment':  'miss in data'}
    if not isinstance(data['comment'], str) and not data['comment'] is None:
        return {'comment': 'is not str type'}

    if not 'manufacturer' in data:
        return {'manufacturer':  'miss in data'}
    if not isinstance(data['manufacturer'], str):
        return {'manufacturer': 'is not str type'}
    
    if not 'name' in data:
        return {'name':  'miss in data'}
    if not isinstance(data['name'], str):
        return {'name': 'is not str type'}
    
    if not 'reserve' in data:
        return {'reserve': 'miss in data'}
    if not isinstance(data['reserve'], int):
        return {'reserve': 'is not int type'}

    if not 'spool_qty' in data:
        return {'spool_qty': 'miss in data'}
    if not isinstance(data['spool_qty'], int):
        return {'spool_qty': 'is not int type'}
    
    if not 'spool_weight' in data:
        return {'spool_weight': 'miss in data'}
    if not isinstance(data['spool_weight'], int):
        return {'spool_weight': 'is not int type'}
    
    if not 'thickness' in data:
        return {'thickness': 'miss in data'}
    if not isinstance(data['thickness'], int):
        return {'thickness': 'is not int type'}
    
    if not 'weight' in data:
        return {'weight': 'miss in data'}
    if not isinstance(data['weight'], int):
        return {'weight': 'is not int type'}
    
    if not 'weight_10m' in data:
        return {'weight_10m': 'miss in data'}
    if not isinstance(data['weight_10m'], (int, float)):
        return {'weight_10m': 'is not int or float type'}
    data['weight_10m'] = round(data['weight_10m'], 2)

    if not 'width' in data:
        return {'width': 'miss in data'}
    if not isinstance(data['width'], int):
        return {'width': 'is not int type'}
    return
    

def errors_validate_consumption(data: dict):
    """validate consumption material"""
    if not 'edit_spool_qty' in data:
        return {'edit_spool_qty': 'miss in data'}
    if not isinstance(data['edit_spool_qty'], int):
        return {'edit_spool_qty': 'is not int type'}
    
    if not 'edit_weight' in data:
        return {'edit_weight': 'miss in data'}
    if not isinstance(data['edit_weight'], int):
        return {'edit_weight': 'is not int type'}
    return