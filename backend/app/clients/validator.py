from sqlalchemy import select
from sqlalchemy.orm import Session
import string, re

from app.clients.models import DB_client
from app import engine


def normalize(key: str, data: dict):
    data[key] = ' '.join([word.capitalize() for word in data[key].split(' ')])
    data[key] = re.sub(r"\'([A-Za-zА-Яа-я])", lambda m: "'" + m.group(1).lower(), data[key])
    data[key] = re.sub(r"\-([A-Za-zА-Яа-я])", lambda m: "-" + m.group(1).capitalize(), data[key])

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
    with Session(engine) as session:

        if not 'address' in data:
            return {'address':  'miss in data'}
        if not isinstance(data['address'], str) and not data['address'] is None:
            return {'address': 'is not str type'}
        
        if not 'city' in data:
            return {'city':  'miss in data'}
        if not isinstance(data['city'], str):
            return {'city': 'is not str type'}
        if data['city']:
            normalize('city', data)

        if 'coach' not in data:
            return {"coach":  "miss in data"}
        if not isinstance(data['coach'], str) and data['coach'] is not None:
            return {'coach': 'is not str type'}
        if data['coach']:
            normalize('coach', data)

        if not 'comment' in data:
            return {"comment":  "miss in data"}
        if not isinstance(data['comment'], str) and not data['comment'] is None:
            return {'comment': 'is not str type'}
        
        if not 'first_name' in data:
            return {"first_name":  "miss in data"}
        if not isinstance(data['first_name'], str):
            return {'first_name': 'is not str type'}
        normalize('first_name', data)

        if not 'second_name' in data:
            return {"second_name":  "miss in data"}
        if not isinstance(data['second_name'], str):
            return {'second_name': 'is not str type'}
        normalize('second_name', data)

        if not 'surname' in data:
            return {"surname":  "miss in data"}
        if not isinstance(data['surname'], str) and not data['surname'] is None:
            return {'surname': 'is not str type'}
        if data['surname']:
            normalize('surname', data)

        if not 'team' in data:
            return {"team":  "miss in data"}
        if not isinstance(data['team'], str) and not data['team'] is None:
            return {'team': 'is not str type'}
        if data['team']:
            normalize('team', data)

        if not 'np_number' in data:
            return {'np_number': 'miss in data'}
        if not isinstance(data['np_number'], int):
            return {'np_number': 'is not int type'}
        
        if not 'phone' in data:
            return {'phone': 'miss in data'}
        if not isinstance(data['phone'], (str, int)):
            return {'phone': 'is not str type'}
        data['phone'] = str(data['phone'])
        data['phone'] = re.sub(r'\D', '', data['phone'])
        
        if not 'zip_code' in data:
            return {'zip_code': 'miss in data'}
        if not isinstance(data['zip_code'], int) and not data['zip_code'] is None:
            return {'zip_code': 'is not int type'}

    return 
