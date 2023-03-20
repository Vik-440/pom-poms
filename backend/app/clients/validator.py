from sqlalchemy import select
from sqlalchemy.orm import Session
import string

from app.clients.models import DB_client
from app import engine


def validate_id_client(id_client: int):
    """Validator for ID client number"""
    with Session(engine) as session:
        if not id_client:
            return {'id_client': 'miss in data'}
        if not isinstance(id_client, int):
            return {'id_client': 'is not int type'}
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == id_client))
        if not session.execute(stmt).first():
            return {'id_client': f'ID client {id_client} is invalid'}
    return


def validate_client(data: dict):
    """Validator for create client"""
    with Session(engine) as session:

        if not 'address' in data:
            return {"address":  "miss in data"}
        if not isinstance(data['address'], str):
            return {'address': 'is not str type'}
        
        if not 'city' in data:
            return {"city":  "miss in data"}
        if not isinstance(data['city'], str):
            return {'city': 'is not str type'}
        data['city'] = string.capwords(data['city'])

        if not 'coach' in data:
            return {"coach":  "miss in data"}
        if not isinstance(data['coach'], str):
            return {'coach': 'is not str type'}
        data['coach'] = data['coach'].capitalize()

        if not 'comment' in data:
            return {"comment":  "miss in data"}
        if not isinstance(data['comment'], str):
            return {'comment': 'is not str type'}
        
        if not 'first_name' in data:
            return {"first_name":  "miss in data"}
        if not isinstance(data['first_name'], str):
            return {'first_name': 'is not str type'}
        data['first_name'] = data['first_name'].capitalize()

        if not 'second_name' in data:
            return {"second_name":  "miss in data"}
        if not isinstance(data['second_name'], str):
            return {'second_name': 'is not str type'}
        data['second_name'] = data['second_name'].capitalize()

        if not 'surname' in data:
            return {"surname":  "miss in data"}
        if not isinstance(data['surname'], str):
            return {'surname': 'is not str type'}
        data['surname'] = data['surname'].capitalize()

        if not 'team' in data:
            return {"team":  "miss in data"}
        if not isinstance(data['team'], str):
            return {'team': 'is not str type'}
        data['team'] = data['team'].capitalize()

        if not 'np_number' in data:
            return {'np_number': 'miss in data'}
        if not isinstance(data['np_number'], int):
            return {'np_number': 'is not int type'}
        
        if not 'phone' in data:
            return {'phone': 'miss in data'}
        if not isinstance(data['phone'], str):
            return {'phone': 'is not int type'}
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.phone == data['phone']))
        if session.execute(stmt).first():
            return {'phone': f'mobile number {data["phone"]} already exists'}
        
        if not 'zip_code' in data:
            return {'zip_code': 'miss in data'}
        if not isinstance(data['zip_code'], int):
            return {'zip_code': 'is not int type'}

    return 
