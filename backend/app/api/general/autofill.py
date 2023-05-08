"""Module autofill fields (clients, products, materials)"""

from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session
import re

from app.products.models import DB_product
from app.clients.models import DB_client
from app.materials.models import DB_materials

from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


def search_by_phone(args):
    """search clients by phone"""
    if 'phone' not in args:
        return None
    
    value = f'%{str(args.get("phone"))}%'

    with Session(engine) as session:
        stmt = (
            select(DB_client.id_client, DB_client.phone)
            .where(DB_client.phone.ilike(value))
            .order_by(DB_client.id_client))
    return [{'id_client': clients.id_client, 'value': clients.phone}\
            for clients in session.execute(stmt).all()]


def search_by_second_name(args):
    """search clients by second_name"""
    if 'second_name' not in args:
        return None
    
    value = f'%{str(args.get("second_name"))}%'

    with Session(engine) as session:
        stmt = (
            select(
                DB_client.id_client,
                DB_client.second_name,
                DB_client.first_name)
            .where(DB_client.second_name.ilike(value))
            .order_by(DB_client.id_client))
    return [{'id_client': clients.id_client, 'value': f'{clients.second_name} {clients.first_name}'}\
            for clients in session.execute(stmt).all()]


def search_by_city(args):
    """search cities"""
    if 'city' not in args:
        return None
    
    value = f'%{str(args.get("city"))}%'

    with Session(engine) as session:
        stmt = (
            select(DB_client.city)
            .where(DB_client.city.ilike(value))
            .order_by(DB_client.city))
        unique_cities = {cities.city for cities in session.execute(stmt).all()}
    return [{'value': city} for city in unique_cities]


def search_by_team(args):
    """search teams"""
    if 'team' not in args:
        return None
    
    value = f'%{str(args.get("team"))}%'

    with Session(engine) as session:
        stmt = (
            select(DB_client.team)
            .where(DB_client.team.ilike(value))
            .order_by(DB_client.team))
        unique_teams = {teams.team for teams in session.execute(stmt).all()}
    return [{'value': team} for team in unique_teams]


def search_by_coach(args):
    """search coach"""
    if 'coach' not in args:
        return None
    
    value = f'%{str(args.get("coach"))}%'

    with Session(engine) as session:
        stmt = (
            select(DB_client.coach)
            .where(DB_client.coach.ilike(value))
            .order_by(DB_client.coach))
        unique_coach = {coaches.coach for coaches in session.execute(stmt).all()}
    return [{'value': coach} for coach in unique_coach]


def search_by_article(args):
    """search by article products"""
    if 'article' not in args:
        return None
    
    value = f'%{str(args.get("article"))}%'
    value = value.upper()
    value = re.sub(r'A', 'А', value)
    value = re.sub(r'B', 'В', value)
    value = re.sub(r'C', 'С', value)

    with Session(engine) as session:
        stmt = (
            select(
                DB_product.id_product,
                DB_product.article)
            .where(DB_product.article.ilike(value))
            .order_by(DB_product.id_product))
    return [{'id_product': products.id_product, 'value': products.article}\
            for products in session.execute(stmt).all()]


def search_by_name_material(args):
    """search by name material"""
    if 'name_material' not in args:
        return None
    
    value = f'%{str(args.get("name_material"))}%'
    value = re.sub(r'A', 'А', value, flags=re.IGNORECASE)
    value = re.sub(r'B', 'В', value, flags=re.IGNORECASE)
    value = re.sub(r'C', 'С', value, flags=re.IGNORECASE)

    with Session(engine) as session:
        stmt = (
            select(
                DB_materials.id_material,
                DB_materials.name)
            .where(DB_materials.name.ilike(value))
            .order_by(DB_materials.id_material))
    return [{'id_material': materials.id_material, 'value': materials.name}\
            for materials in session.execute(stmt).all()]


@api.route('/autofill', methods=['GET'])
@swag_from('/docs/get_autofill_product_client_material.yml')
def autofill_fields():
    """Autofill fields"""
    args = request.args
    keys = [
        'phone',
        'second_name',
        'city',
        'team',
        'coach',
        'article',
        'name_material']

    try:
        if not args:
            return jsonify({'args': keys}), 200
        
        search_functions = [
            search_by_phone,
            search_by_second_name,
            search_by_city,
            search_by_team,
            search_by_coach,
            search_by_article,
            search_by_name_material]
        for search_func in search_functions:
            result = search_func(args)
            if result is not None:
                return jsonify(result)

        return jsonify({'autofill': 'request does not have searching keys'}), 200

    except Exception as e: # pragma: no cover
        logger.info(f'mistake autofill: {e}')
        return jsonify(f'autofill: {e}'), 400
