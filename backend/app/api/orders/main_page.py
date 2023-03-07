# import json
from datetime import datetime
from flask import request, jsonify
from sqlalchemy import func, select, or_, and_#, join, table
from sqlalchemy.orm import Session, aliased
from collections import namedtuple

from app.orders.models import DB_orders
from app.clients.models import DB_client
from app.products.models import DB_product
from app.payments.models import DB_payment
from app import engine
from .. import api

from log.logger import logger


def getting_args(args: dict) -> tuple:
    data_today = datetime.today().strftime('%Y-%m-%d')
    data_start_search = args.get('start_date', '2016-01-01')
    data_finish_search = args.get('data_finish', data_today)
    status_order = args.get('fulfilled', 'False')
    return data_start_search, data_finish_search, status_order


def getting_filter_clients(args: dict) -> list:
    client_alias = aliased(DB_client)
    recipient_alias = aliased(DB_client)
    filters_clients = {
                'phone_client': DB_client.phone,
                'id_client': DB_client.id_client,
                'team': DB_client.team,
                'coach': DB_client.coach,
                'sity': DB_client.city}
    id_client_list = []
    for key, value in filters_clients.items():
        if key in args:
            stmt = (
                select(DB_orders.id_order)
                .join(client_alias, DB_orders.id_client == client_alias.id_client)
                .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
                .join(DB_client, DB_orders.id_client == DB_client.id_client)
                .where(value == args[key])
                .order_by(DB_client.id_client))
            with Session(engine) as session:
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
    return id_client_list


def getting_filter_products(args: dict) -> list:
    fillters_products = {
                'kod_model': DB_product.article,
                'kod_model_like': DB_product.article,
                'kolor_model_like': DB_product.colors}            
    id_products_list = []
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
            with Session(engine) as session:
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_products_list.append(row)
    # print(id_products_list)
    return id_products_list




@api.route('/main', methods=['GET'])
def main_page():
    """Preparing main page with or without same requests"""
    args = request.args
    logger.info(f'Get main works in API with args: {args}')

    try:
        with Session(engine) as session:
            data_start_search, data_finish_search, status_order = getting_args(args)

            id_client_list = getting_filter_clients(args)
            id_products_list = getting_filter_products(args)


            id_orders = []
            for id_model_cucle in id_products_list:
                stmt = (
                    select(DB_orders.id_order)
                    .where(DB_orders.id_models.any(id_model_cucle)))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_orders.append(row)
            # print(id_client_list)
            # print(id_products_list)
            # print(id_orders)
            if id_client_list and id_orders:
                orders = [x for x in id_client_list if x in id_orders]
            else:
                orders = id_client_list + id_orders
# ###########################################################################
            stmt = (
                select(
                    DB_product.id_product,
                    DB_product.article,
                    DB_product.colors,
                    DB_product.comment)
                .order_by(DB_product.id_product))
            data_models = {}
            models = session.execute(stmt).all()
            for model in models:
                data_models.update({
                    model.id_product: [model.article, model.colors, model.comment]
                })
# ###########################################################################
            client_alias = aliased(DB_client)
            recipient_alias = aliased(DB_client)
               
            select_modul = (select(
                func.sum(DB_payment.payment).label('my_sum'),
                DB_orders.id_order,
                DB_orders.comment,
                DB_orders.data_create,
                DB_orders.data_plane_send,
                DB_orders.status_order,
                DB_orders.sum_payment,
                DB_orders.discont,
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

            select_modul = select_modul.where(
                                DB_orders.data_create >= data_start_search,
                                DB_orders.data_create <= data_finish_search)

            print(orders)
            print(status_order)
            if not orders and status_order == 'false':
                stmt = (
                    select_modul
                    # .where(DB_orders.id_order.in_(orders))
                    .where(DB_orders.status_order == status_order)
                    .order_by(DB_orders.data_plane_send))

            elif status_order == 'all':
                stmt = (
                    select_modul
                    .where(DB_orders.id_order.in_(orders))
                    .order_by(DB_orders.id_order))
                # if id_client_list and not id_orders:
                #     stmt = select_modul.where(
                #         or_(
                #             DB_orders.id_client.in_(id_client_list),
                #             DB_orders.id_recipient.in_(id_client_list)))\
                #         .order_by(DB_orders.id_order)
                # elif id_orders and not id_client_list:
                #     stmt = select_modul.where(
                #        DB_orders.id_order.in_(id_orders))\
                #         .order_by(DB_orders.id_order)
                # elif id_orders and id_client_list:
                #     stmt = select_modul.where(
                #         and_(
                #             DB_orders.id_order.in_(id_orders),
                #             or_(
                #                 DB_orders.id_client.in_(id_client_list),
                #                 DB_orders.id_recipient.in_(id_client_list))))\
                #         .order_by(DB_orders.id_order)
                # else:
                #     stmt = select_modul.order_by(DB_orders.id_order)
            # elif status_order == 'true':
            else:
                stmt = (
                    select_modul
                    .where(DB_orders.id_order.in_(orders))
                    .where(DB_orders.status_order == status_order)
                    .order_by(DB_orders.id_order))
            # else:
            #     stmt = (
            #         select_modul
            #         # .where(DB_orders.id_order.in_(orders))
            #         .where(DB_orders.status_order == status_order)
            #         .order_by(DB_orders.data_plane_send))
                # if id_client_list and not id_orders:
                #     stmt = select_modul.where(
                #         DB_orders.status_order == status_order,
                #         or_(
                #             DB_orders.id_client.in_(id_client_list),
                #             DB_orders.id_recipient.in_(id_client_list)))\
                #         .order_by(DB_orders.id_order)
                # elif id_orders and not id_client_list:
                #     stmt = select_modul.where(
                #         DB_orders.status_order == status_order,
                #         DB_orders.id_order.in_(id_orders))\
                #         .order_by(DB_orders.id_order)
                # elif id_orders and id_client_list:
                #     stmt = select_modul.where(
                #         DB_orders.status_order == status_order,
                #         and_(
                #             DB_orders.id_order.in_(id_orders),
                #             or_(
                #                 DB_orders.id_client.in_(id_client_list),
                #                 DB_orders.id_recipient.in_(id_client_list))))\
                #         .order_by(DB_orders.id_order)
                # else:
                #     if status_order == 'true':
                #         stmt = select_modul.where(
                #             DB_orders.status_order == status_order)\
                #             .order_by(DB_orders.id_order)
                #     else:
                #         stmt = (select_modul
                #             .where(DB_orders.status_order == status_order)
                #             .order_by(DB_orders.data_plane_send))

            list_order = session.execute(stmt).all()
            if not list_order:
                stmt = select(func.max(DB_orders.id_order))
                last_order = session.execute(stmt).scalar_one()
                stmt = select_modul.where(DB_orders.id_order == last_order)
                list_order = session.execute(stmt).all()
#
            full_block = []
            for row in list_order:
                id_order = row.id_order
                comment = row.comment
                data_create = (str(row.data_create))
                data_plane_send = (str(row.data_plane_send))
                status_order = (row.status_order)
                sum_payment = (row.sum_payment - row.discont)
                qty_pars = (row.qty_pars)
                phase_1 = row.phase_1
                phase_2 = row.phase_2
                phase_3 = row.phase_3
                id_models = row.id_models
                phone_client = row.phone_order
                second_name = row.second_name
                first_name = row.first_name
                phone = row.phone
                np_number = row.np_number
                zip_code = row.zip_code
                address = row.address
                city = row.city
                real_money = row.my_sum
#
                colors, article, comment_product, = [], [], []

                for model in id_models:
                    article.append(data_models.get(model)[0])
                    colors.append(data_models.get(model)[1])
                    comment_product.append(data_models.get(model)[2])

                if len(list(qty_pars)) == 1:
                    qty_pars = qty_pars[0]
                    phase_1 = phase_1[0]
                    phase_2 = phase_2[0]
                    phase_3 = phase_3[0]
                    colors = colors[0]
                    article = article[0]
                    comment_product = comment_product[0]
#
                one_block = {
                    "id_order": id_order,
                    "comment_order": comment,
                    "data_order": data_create,
                    "kolor_model": colors,
                    "kod_model": article,
                    "comment_model": comment_product,
                    "quantity_pars_model": qty_pars,
                    "phase_1": phase_1,
                    "phase_2": phase_2,
                    "phase_3": phase_3,
                    "sum_payment": sum_payment,
                    "real_money": real_money,
                    "phone_client": phone_client,
                    "phone_recipient": phone,
                    "sity": city,
                    "data_plane_order": data_plane_send,
                    "fulfilled_order": status_order,
                    "np_number": np_number,
                    "zip_code": zip_code,
                    "street_house_apartment": address,
                    "second_name_client": second_name,
                    "first_name_client": first_name
                    }
                full_block.append(one_block)
        # print(full_block)
        return jsonify(full_block)
    except Exception as e:
        return jsonify(f'Error in function main_page: {e}')
