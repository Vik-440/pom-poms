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


def validate_id_color_and_part(data, key_id_color, key_part):
    with Session(engine) as session:
        if data[key_id_color] is not None:
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data[key_id_color]))
            if not session.execute(stmt).first():
                return {key_id_color: f'{key_id_color} {data[key_id_color]} is missing'}

            error = validate_field(key_part, int, data)
            if error:
                return error

            data[key_part] = min(data[key_part], 100)
        else:
            for key in [key_part] + [f'id_color_{i}' for i in range(int(key_id_color[-1]) + 1, 5)] + [f'part_{i}' for i in range(int(key_part[-1]) + 1, 5)]:
                data[key] = None


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
        ('id_color_4', (int, type(None)))]
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

        for key_id_color, key_part in [('id_color_2', 'part_2'), ('id_color_3', 'part_3'), ('id_color_4', 'part_4')]:
            error = validate_id_color_and_part(data, key_id_color, key_part)
            if error:
                return error
    return 
