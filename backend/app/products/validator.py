from sqlalchemy import select
from sqlalchemy.orm import Session
import re

from app.products.models import DB_product
from app.materials.models import DB_materials
from utils.validators import validate_field
from app import engine


def validate_id_product(id_product: int):
    """Validator for ID product number"""
    with Session(engine) as session:
        stmt = (
            select(DB_product.id_product)
            .where(DB_product.id_product == id_product))
        if not session.execute(stmt).first():
            return {'id_product': f'ID product {id_product} is invalid'}
    return


def validate_article_product(data: dict):
    """Validator for article product"""
    with Session(engine) as session:
        stmt = (
            select(DB_product.article)
            .where(DB_product.article == data['article']))
        if session.execute(stmt).first():
            return {'article': f'article {data["article"]} already exists'}
    return


def validate_product(data: dict):
    """Validator for create product"""
    fields_to_check = [
        ('article', str),
        ('colors', str),
        ('comment', (str, type(None))),
        ('price', int),
        ('id_color_1', int),
        ('part_1', int),
        ('id_color_2', (int, type(None))),
        ('id_color_3', (int, type(None))),
        ('id_color_4', (int, type(None))),
    ]
    for field, field_type in fields_to_check:
        error = validate_field(field, field_type, data)
        if error:
            return error
        
    with Session(engine) as session:
        pattern = r'^\d{3}-'
        if not (re.match(pattern, data['article'])):
            return {'article': 'is not correct'}
        data['article'] = data['article'].upper()
        data['article'] = re.sub(r'A', 'А', data['article'])
        data['article'] = re.sub(r'B', 'В', data['article'])
        data['article'] = re.sub(r'C', 'С', data['article'])

        if len(data['colors']) < 5:
            return {'colors': "can't be less than 5 characters"}

        stmt = (
            select(DB_materials.id_material)
            .where(DB_materials.id_material == data['id_color_1']))
        if not session.execute(stmt).first():
            return {'id_color_1': f'id_color_1 {data["id_color_1"]} is missing'}
        
        data['part_1'] = min(data['part_1'], 100)

        if not data['id_color_2'] is None:
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_2']))
            if not session.execute(stmt).first():
                return {'id_color_2': f'id_color_2 {data["id_color_2"]} is missing'}
        
            if not 'part_2' in data:
                return {'part_2': 'miss in data'}
            if not isinstance(data['part_2'], int):
                return {'part_2': 'is not int type'}
            data['part_2'] = min(data['part_2'], 100)
        else:
            data['part_2'] = None
            data['id_color_3'] = None
            data['part_3'] = None
            data['id_color_4'] = None
            data['part_4'] = None

        if not data['id_color_3'] is None:
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_3']))
            if not session.execute(stmt).first():
                return {'id_color_3': f'id_color_3 {data["id_color_3"]} is missing'}
        
            if not 'part_3' in data:
                return {'part_3': 'miss in data'}
            if not isinstance(data['part_3'], int):
                return {'part_3': 'is not int type'}
            data['part_3'] = min(data['part_3'], 100)
        else:
            data['part_3'] = None
            data['id_color_4'] = None
            data['part_4'] = None
            
        if not data['id_color_4'] is None:
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_4']))
            if not session.execute(stmt).first():
                return {'id_color_4': f'id_color_4 {data["id_color_4"]} is missing'}
        
            if not 'part_4' in data:
                return {'part_4': 'miss in data'}
            if not isinstance(data['part_4'], int):
                return {'part_4': 'is not int type'}
            data['part_4'] = min(data['part_4'], 100)
        else:
            data['part_4'] = None

    return 
