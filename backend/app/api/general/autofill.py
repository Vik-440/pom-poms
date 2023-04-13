"""Module autofill fields (clients, products, materials)"""

from flask import request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import select

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
    if not 'phone' in args:
        return None
    value = ('%' + str(args.get('phone')) + '%')
    clients = []
    with Session(engine) as session:
        stmt = (
            select(DB_client.id_client, DB_client.phone)
            .where(DB_client.phone.ilike(value))
            .order_by(DB_client.id_client))
        _ = session.execute(stmt).all()
        for client in _:
            clients.append({
                'id_client': client.id_client,
                'value': client.phone})
    return clients


def search_by_second_name(args):
    """search clients by second_name"""
    if not 'second_name' in args:
        return None
    value = ('%' + str(args.get('second_name')) + '%')
    clients = []
    with Session(engine) as session:
        stmt = (
            select(
                DB_client.id_client,
                DB_client.second_name,
                DB_client.first_name)
            .where(DB_client.second_name.ilike(value))
            .order_by(DB_client.id_client))
        _ = session.execute(stmt).all()
        for client in _:
            clients.append({
                'id_client': client.id_client,
                'value': f'{client.second_name} {client.first_name}'})
    return clients


def search_by_city(args):
    """search cities"""
    if not 'city' in args:
        return None
    value = ('%' + str(args.get('city')) + '%')
    unique_cities = set()
    with Session(engine) as session:
        stmt = (
            select(DB_client.city)
            .where(DB_client.city.ilike(value))
            .order_by(DB_client.city))
        _ = session.execute(stmt).all()
        for city in _:
            unique_cities.add(city.city)
        cities = [{'value': city} for city in unique_cities]
    return cities


def search_by_team(args):
    """search teams"""
    if not 'team' in args:
        return None
    value = ('%' + str(args.get('team')) + '%')
    unique_teams = set()
    with Session(engine) as session:
        stmt = (
            select(DB_client.team)
            .where(DB_client.team.ilike(value))
            .order_by(DB_client.team))
        _ = session.execute(stmt).all()
        for team in _:
            unique_teams.add(team.team)
        teams = [{'value': team} for team in unique_teams]
    return teams


def search_by_coach(args):
    """search coach"""
    if not 'coach' in args:
        return None
    value = ('%' + str(args.get('coach')) + '%')
    unique_coach = set()
    with Session(engine) as session:
        stmt = (
            select(DB_client.coach)
            .where(DB_client.coach.ilike(value))
            .order_by(DB_client.coach))
        _ = session.execute(stmt).all()
        for coach in _:
            unique_coach.add(coach.coach)
        coachs = [{'value': coach} for coach in unique_coach]
    return coachs


def search_by_article(args):
    """search by article products"""
    if not 'article' in args:
        return None
    
    value = ('%' + str(args.get('article')) + '%')
    value = value.upper()
    value = re.sub(r'A', 'А', value)
    value = re.sub(r'B', 'В', value)
    value = re.sub(r'C', 'С', value)

    products = []
    with Session(engine) as session:
        stmt = (
            select(
                DB_product.id_product,
                DB_product.article)
            .where(DB_product.article.ilike(value))
            .order_by(DB_product.id_product))
        _ = session.execute(stmt).all()
        for product in _:
            products.append({
                'id_product': product.id_product,
                'value': product.article})
    return products


def search_by_name_material(args):
    """search by name material"""
    if not 'name_material' in args:
        return None
    
    value = ('%' + str(args.get('name_material')) + '%')
    value = re.sub(r'A', 'А', value, flags=re.IGNORECASE)
    value = re.sub(r'B', 'В', value, flags=re.IGNORECASE)
    value = re.sub(r'C', 'С', value, flags=re.IGNORECASE)

    name_materials = []
    with Session(engine) as session:
        stmt = (
            select(
                DB_materials.id_material,
                DB_materials.name)
            .where(DB_materials.name.ilike(value))
            .order_by(DB_materials.id_material))
        _ = session.execute(stmt).all()
        for name_material in _:
            name_materials.append({
                'id_material': name_material.id_material,
                'value': name_material.name})
    return name_materials


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

        return jsonify({'autofill': 'request does not have searching keys'}), 400

    except Exception as e: # pragma: no cover
        logger.info(f'misstake autofill: {e}') # pragma: no cover
        return jsonify(f'autofill: {e}'), 400 # pragma: no cover
