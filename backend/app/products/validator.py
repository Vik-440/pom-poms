from sqlalchemy import select
from sqlalchemy.orm import Session
import string, re

from app.products.models import DB_product
from app.materials.models import DB_materials
from app import engine


def validate_id_product(id_product: int):
    """Validator for ID product number"""
    with Session(engine) as session:
        if not id_product:
            return {'id_product': 'miss in data'}
        if not isinstance(id_product, int):
            return {'id_product': 'is not int type'}
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
    with Session(engine) as session:
        if not 'article' in data:
            return {"article":  "miss in data"}
        if not isinstance(data['article'], str):
            return {'article': 'is not str type'}
        data['article'] = data['article'].upper()
        data['article'] = re.sub(r'A', 'А', data['article'])
        data['article'] = re.sub(r'B', 'В', data['article'])
        data['article'] = re.sub(r'C', 'С', data['article'])

        if not 'colors' in data:
            return {"colors":  "miss in data"}
        if not isinstance(data['colors'], str):
            return {'colors': 'is not str type'}

        if not 'comment' in data:
            return {'comment':  "miss in data"}
        if not isinstance(data['comment'], str) and not data['comment'] is None:
            return {'comment': 'is not str type'}
        
        if not 'price' in data:
            return {'price': 'miss in data'}
        if not isinstance(data['price'], int):
            return {'price': 'is not int type'}

        if not 'id_color_1' in data:
            return {'id_color_1': 'miss in data'}
        if not isinstance(data['id_color_1'], int):
            return {'id_color_1': 'is not int type'}
        stmt = (
            select(DB_materials.id_material)
            .where(DB_materials.id_material == data['id_color_1']))
        if not session.execute(stmt).first():
            return {'id_color_1': f'id_color_1 {data["id_color_1"]} is missing'}
        
        if not 'id_part_1' in data:
            return {'id_part_1': 'miss in data'}
        if not isinstance(data['id_part_1'], int):
            return {'id_part_1': 'is not int type'}
        if data['id_part_1'] > 100:
            data['id_part_1'] = 100

        if 'id_color_2' in data and not data['id_color_2'] is None:
            if not isinstance(data['id_color_2'], int):
                return {'id_color_2': 'is not int type'}
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_2']))
            if not session.execute(stmt).first():
                return {'id_color_2': f'id_color_2 {data["id_color_2"]} is missing'}
        
            if not 'id_part_2' in data:
                return {'id_part_2': 'miss in data'}
            if not isinstance(data['id_part_2'], int):
                return {'id_part_2': 'is not int type'}
            if data['id_part_2'] > 100:
                data['id_part_2'] = 100
        else:
            data['id_color_2'] = None
            data['id_part_2'] = None
            data['id_color_3'] = None
            data['id_part_3'] = None
            data['id_color_4'] = None
            data['id_part_4'] = None

        if 'id_color_3' in data and not data['id_color_3'] is None:
            if not isinstance(data['id_color_3'], int):
                return {'id_color_3': 'is not int type'}
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_3']))
            if not session.execute(stmt).first():
                return {'id_color_3': f'id_color_3 {data["id_color_3"]} is missing'}
        
            if not 'id_part_3' in data:
                return {'id_part_3': 'miss in data'}
            if not isinstance(data['id_part_3'], int):
                return {'id_part_3': 'is not int type'}
            if data['id_part_3'] > 100:
                data['id_part_3'] = 100
        else:
            data['id_color_3'] = None
            data['id_part_3'] = None
            data['id_color_4'] = None
            data['id_part_4'] = None
            
        if 'id_color_4' in data and not data['id_color_4'] is None:
            if not isinstance(data['id_color_4'], int):
                return {'id_color_4': 'is not int type'}
            stmt = (
                select(DB_materials.id_material)
                .where(DB_materials.id_material == data['id_color_4']))
            if not session.execute(stmt).first():
                return {'id_color_4': f'id_color_4 {data["id_color_4"]} is missing'}
        
            if not 'id_part_4' in data:
                return {'id_part_4': 'miss in data'}
            if not isinstance(data['id_part_4'], int):
                return {'id_part_4': 'is not int type'}
            if data['id_part_4'] > 100:
                data['id_part_4'] = 100
        else:
            data['id_color_4'] = None
            data['id_part_4'] = None

    return 
