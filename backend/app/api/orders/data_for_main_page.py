"""Main module for creating data for main page with or withot filters"""

from datetime import datetime
from flask import request, jsonify
from sqlalchemy import func, select#, or_, and_, join, table
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
                'sity': DB_client.city}
    id_orders_client = []
    with Session(engine) as session:
        for key, value in filters_clients.items():
            if key in args:
                stmt = (
                    select(DB_orders.id_order)
                    .join(client_alias, DB_orders.id_client == client_alias.id_client)
                    .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
                    .join(DB_client, DB_orders.id_client == DB_client.id_client)
                    .where(value == args[key])
                    .order_by(DB_client.id_client))
                pre_list = session.execute(stmt).scalars()
                for order in pre_list:
                    id_orders_client.append(order)
    return id_orders_client


def getting_filter_products(args: dict) -> list:
    """Getting orders with searching products into"""
    fillters_products = {
                'kod_model': DB_product.article,
                'kod_model_like': DB_product.article,
                'kolor_like': DB_product.colors}            
    id_products_list = []
    with Session(engine) as session:
        for key, value in fillters_products.items():
            if key in args:
                if key == 'kod_model':
                    stmt = (
                        select(DB_product.id_product)
                        .where(value == args[key])
                        .order_by(DB_product.id_product))
                else:
                    value = ('%' + str(args.get(key)) + '%')
                    stmt = (
                        select(DB_product.id_product)
                        .where(fillters_products[key].ilike(value))
                        .order_by(DB_product.id_product))
                pre_list = session.execute(stmt).scalars()
                for id_product in pre_list:
                    id_products_list.append(id_product)
        id_orders_products = []
        for id_model_cucle in id_products_list:
            stmt = (
                select(DB_orders.id_order)
                .where(DB_orders.id_models.any(id_model_cucle)))
            pre_list = session.execute(stmt).scalars()
            for order in pre_list:
                id_orders_products.append(order)
    return id_orders_products


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
        products = {}
        models = session.execute(stmt).all()
        for model in models:
            products.update({
                model.id_product: [model.article, model.colors, model.comment]
            })
    return products


def create_select_modul():
    """Creating SELECT for request in DB for main table"""
    client_alias = aliased(DB_client)
    recipient_alias = aliased(DB_client)
    select_modul = (select(
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
    

    return select_modul


@api.route('/main', methods=['GET'])
@swag_from('/docs/get_main.yml')
def main_page():
    """Preparing main page with or without same requests"""
    args = request.args
    logger.info(f'Get main works in API with args: {args}')

    try:
        with Session(engine) as session:
            date_start_search, date_finish_search, status_order = getting_args_general(args)

            id_orders_client = getting_filter_clients(args)
            id_orders_products = getting_filter_products(args)
            products = getting_products()
            select_modul_without_date = create_select_modul()
            select_modul = select_modul_without_date.where(
                        DB_orders.date_create >= date_start_search,
                        DB_orders.date_create <= date_finish_search)
            if id_orders_client and id_orders_products:
                orders = list(set(id_orders_client) & set(id_orders_products))
                # orders = [x for x in id_orders_client if x in id_orders_products]
            else:
                orders = id_orders_client + id_orders_products
            
            if not orders and status_order == 'false':
                stmt = (
                    select_modul
                    .where(DB_orders.status_order == status_order)
                    .order_by(DB_orders.date_plane_send, DB_orders.id_order))
            elif status_order == 'all':
                if not orders:
                    stmt = (
                        select_modul
                        .order_by(DB_orders.id_order))
                else:
                    stmt = (
                        select_modul
                        .where(DB_orders.id_order.in_(orders))
                        .order_by(DB_orders.id_order))
            else:
                if not orders:
                    stmt = (
                        select_modul
                        # .where(DB_orders.id_order.in_(orders))
                        .where(DB_orders.status_order == status_order)
                        .order_by(DB_orders.id_order))
                else:
                    stmt = (
                        select_modul
                        .where(DB_orders.id_order.in_(orders))
                        .where(DB_orders.status_order == status_order)
                        .order_by(DB_orders.id_order))
            list_order = session.execute(stmt).all()

            if not list_order:
                subq = select(func.max(DB_orders.id_order)).scalar_subquery()
                stmt = select_modul_without_date.where(DB_orders.id_order == subq)
                list_order = session.execute(stmt).all()

            full_block = []
            for row in list_order:
                colors, article, comment_product, = [], [], []
                id_models = row.id_models
                for model in id_models:
                    article.append(products.get(model)[0])
                    colors.append(products.get(model)[1])
                    comment_product.append(products.get(model)[2])
                
                qty_pars = (row.qty_pars)
                phase_1 = row.phase_1
                phase_2 = row.phase_2
                phase_3 = row.phase_3
                if len(qty_pars) == 1:
                    qty_pars, phase_1, phase_2, phase_3, colors, article, comment_product =\
                        qty_pars[0], phase_1[0], phase_2[0], phase_3[0],\
                        colors[0], article[0], comment_product[0]
                
                full_block.append({
                    "id_order": row.id_order,
                    "comment_order": row.comment,
                    "data_order": (str(row.date_create)),
                    "kolor_model": colors,
                    "kod_model": article,
                    "comment_model": comment_product,
                    "quantity_pars_model": qty_pars,
                    "phase_1": phase_1,
                    "phase_2": phase_2,
                    "phase_3": phase_3,
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

        return jsonify(full_block)
    except Exception as e:
        return jsonify(f'Error in function main_page: {e}')
