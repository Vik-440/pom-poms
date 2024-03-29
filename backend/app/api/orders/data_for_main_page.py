"""Main module for creating data for main page with or without filters"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import func, select, or_, union, and_
from sqlalchemy.orm import Session, aliased

from app.orders.models import DB_orders
from app.clients.models import DB_client
from app.products.models import DB_product
from app.payments.models import DB_payment
from app import engine
from .. import api

from log.logger import logger
from flasgger import swag_from


def getting_args_general(args: dict) -> tuple:
    """"Set general filters into request"""
    date_today = datetime.today().strftime('%Y-%m-%d')
    date_start_search = args.get('data_start', '2016-01-01')
    date_finish_search = args.get('data_end', date_today)
    status_order = args.get('fulfilled', 'false')
    return date_start_search, date_finish_search, status_order


def getting_filter_clients(args: dict) -> list:
    """Getting orders with searching clients into"""
    client_alias = aliased(DB_client)
    recipient_alias = aliased(DB_client)
    filters_clients = {
                'phone_client': DB_client.phone,
                'id_client': DB_client.id_client,
                'team': DB_client.team,
                'coach': DB_client.coach,
                'city': DB_client.city}
    id_orders_client = []
    with Session(engine) as session:
        for key, value in filters_clients.items():
            if key in args:
                stmt1 = (
                    select(DB_orders.id_order)
                    .join(client_alias, DB_orders.id_client == client_alias.id_client)
                    .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
                    .join(DB_client, DB_orders.id_client == DB_client.id_client)
                    .where(value == args[key])
                    .order_by(DB_orders.id_order))
                stmt2= ( select(DB_orders.id_order)
                    .join(client_alias, DB_orders.id_client == client_alias.id_client)
                    .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
                    .join(DB_client, DB_orders.id_recipient == DB_client.id_client)
                    .where(value == args[key])
                    .order_by(DB_orders.id_order))
                stmt = union(stmt1, stmt2).order_by(DB_orders.id_order)
                result = session.execute(stmt).scalars()
                id_orders_client = [id_client for id_client in result] if result is not None else []
    return id_orders_client


def getting_filter_products(args: dict) -> list:
    """Getting orders with searching products into"""
    filters_products = {
        'kod_model': DB_product.article,
        'kod_model_like': DB_product.article,
        'kolor_like': DB_product.colors}

    id_orders_products = set()

    with Session(engine) as session:
        for key, value in filters_products.items():
            if key in args:
                stmt = select(DB_product.id_product).order_by(DB_product.id_product)

                if key == 'kod_model':
                    stmt = stmt.where(value == args[key])
                else:
                    search_value = f"%{args.get(key)}%"
                    stmt = stmt.where(value.ilike(search_value))
                result = session.execute(stmt).scalars()

                id_products = [id_product for id_product in result] if result is not None else []

                for id_model_cycle in id_products:
                    stmt = select(DB_orders.id_order).where(DB_orders.id_models.any(id_model_cycle))
                    result = session.execute(stmt).scalars()
                    id_orders_products.update([id_order for id_order in result] if result is not None else [])

    return list(id_orders_products)



def getting_products() -> dict:
    """Preparing dict of products from DB"""
    with Session(engine) as session:
        stmt = (
            select(
                DB_product.id_product,
                DB_product.article,
                DB_product.colors,
                DB_product.comment)
            .order_by(DB_product.id_product))
        models = session.execute(stmt).all()
    return {model.id_product: [model.article, model.colors, model.comment] for model in models}


def create_select_module():
    """Creating SELECT for request in DB for main table"""
    client_alias = aliased(DB_client)
    recipient_alias = aliased(DB_client)
    select_module = (select(
        func.sum(DB_payment.payment).label('my_sum'),
        DB_orders.id_order,
        DB_orders.comment,
        DB_orders.date_create,
        DB_orders.date_plane_send,
        DB_orders.status_order,
        DB_orders.sum_payment,
        DB_orders.discount,
        DB_orders.qty_pars,
        DB_orders.phase_1,
        DB_orders.phase_2,
        DB_orders.phase_3,
        DB_orders.id_models,
        client_alias.phone.label('phone_order'),
        recipient_alias.second_name,
        recipient_alias.first_name,
        recipient_alias.phone,
        recipient_alias.np_number,
        recipient_alias.zip_code,
        recipient_alias.address,
        recipient_alias.city)
        .group_by(
            DB_orders,
            client_alias,
            recipient_alias)
        .join(client_alias, DB_orders.id_client == client_alias.id_client)
        .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
        .outerjoin(DB_payment, DB_orders.id_order == DB_payment.id_order))
    return select_module


@api.route('/main', methods=['GET'])
@swag_from('/docs/get_main.yml')
def main_page():
    """Preparing main page with or without same requests"""
    args = request.args
    try:
        with Session(engine) as session:
            date_start_search, date_finish_search, status_order = getting_args_general(args)

            id_orders_client = getting_filter_clients(args)
            id_orders_products = getting_filter_products(args)
            products = getting_products()
            select_module_without_date = create_select_module()
            select_module = select_module_without_date.where(
                DB_orders.date_create.between(date_start_search, date_finish_search))
            # print(f'id_orders_client - {id_orders_client}')
            # print(f'id_orders_products - {id_orders_products}')

            if id_orders_client and id_orders_products:
                orders = list(set(id_orders_client) & set(id_orders_products))
            elif id_orders_client or id_orders_products:
                orders = id_orders_client + id_orders_products
            else:
                orders = []
            # print(f'orders - {orders}')
            # print(f'status_order - {status_order}')
            if not orders and status_order == 'false' and date_start_search == '2016-01-01':
                stmt = (
                    select_module
                    .where(DB_orders.status_order == status_order)
                    .order_by(DB_orders.date_plane_send, DB_orders.id_order))
            elif status_order == 'all':
                if not orders:
                    stmt = (
                        select_module
                        .order_by(DB_orders.id_order))
                else:
                    stmt = (
                        select_module
                        .where(DB_orders.id_order.in_(orders))
                        .order_by(DB_orders.id_order))
            else:
                if not orders:
                    stmt = (
                        select_module
                        .where(DB_orders.status_order == status_order)
                        .order_by(DB_orders.id_order))
                else:
                    stmt = (
                        select_module
                        .where(DB_orders.id_order.in_(orders))
                        .where(DB_orders.status_order == status_order)
                        .order_by(DB_orders.id_order))
            stmt = stmt.limit(100)
            list_order = session.execute(stmt).all()

            if not list_order:
                subq = select(func.max(DB_orders.id_order)).scalar_subquery()
                stmt = select_module_without_date.where(DB_orders.id_order == subq)
                list_order = session.execute(stmt).all()

            full_block = []
            for row in list_order:
                colors, article, comment_product, = [], [], []
                id_models = row.id_models
                for model in id_models:
                    article.append(products.get(model)[0])
                    colors.append(products.get(model)[1])
                    comment_product.append(products.get(model)[2])
                
                full_block.append({
                    "id_order": row.id_order,
                    "comment_order": row.comment,
                    "data_order": (str(row.date_create)),
                    "kolor_model": colors,
                    "kod_model": article,
                    "comment_model": comment_product,
                    "quantity_pars_model": row.qty_pars,
                    "phase_1": row.phase_1,
                    "phase_2": row.phase_2,
                    "phase_3": row.phase_3,
                    "sum_payment": (row.sum_payment - row.discount),
                    "real_money": row.my_sum,
                    "phone_client": row.phone_order,
                    "phone_recipient": row.phone,
                    "sity": row.city,
                    "data_plane_order": (str(row.date_plane_send)),
                    "fulfilled_order": row.status_order,
                    "np_number": row.np_number,
                    "zip_code": row.zip_code,
                    "street_house_apartment": row.address,
                    "second_name_client": row.second_name,
                    "first_name_client": row.first_name})

        return jsonify(full_block), 200
    except Exception as e: # pragma: no cover
        logger.exception(e)
        return jsonify(f'Error in function main_page: {e}'), 400
