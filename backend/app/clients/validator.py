from sqlalchemy import select
from sqlalchemy.orm import Session
import re

from app.clients.models import DB_client
from utils.validators import validate_field
from app import engine


def normalize_fields(data, fields_to_normalize):
    """Normalise data for product"""
    for field in fields_to_normalize:
        if data[field]:
            data[field] = ' '.join([word.capitalize() for word in data[field].split(' ')])
            data[field] = re.sub(r"\'([A-Za-zА-Яа-я])", lambda m: "'" + m.group(1).lower(), data[field])
            data[field] = re.sub(r"\-([A-Za-zА-Яа-я])", lambda m: "-" + m.group(1).capitalize(), data[field])


def validate_id_client(id_client: int):
    """Validator for ID client number"""
    with Session(engine) as session:
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == id_client))
        if not session.execute(stmt).first():
            return {'id_client': f'ID client {id_client} is invalid'}
    return


def validate_number(data: dict):
    """Validator number client"""
    with Session(engine) as session:
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.phone == data['phone']))
        if session.execute(stmt).first():
            return {'phone': f'mobile number {data["phone"]} already exists'}
    return


def validate_client(data: dict):
    """Validator for create client"""
    fields_to_check = [
        ('address', (str, type(None))),
        ('city', str),
        ('coach', (str, type(None))),
        ('comment', (str, type(None))),
        ('first_name', str),
        ('second_name', str),
        ('surname', (str, type(None))),
        ('team', (str, type(None))),
        ('np_number', int),
        ('phone', (str, int)),
        ('zip_code', (int, type(None)))]
    for field, field_type in fields_to_check:
        error = validate_field(field, field_type, data)
        if error:
            return error
    fields_to_normalize = [
        'city',
        'first_name',
        'second_name',
        'coach',
        'surname',
        'team']
    normalize_fields(data, fields_to_normalize)
    data['phone'] = str(data['phone'])
    data['phone'] = re.sub(r'\D', '', data['phone'])

    return
