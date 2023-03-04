import json
from datetime import datetime
from flask import request, jsonify
from sqlalchemy import func, select, or_, and_, join, table
from sqlalchemy.orm import Session, aliased

from app.orders.models import DB_orders
from app.clients.models import DB_client
from app.products.models import DB_product
from app.payments.models import DB_payment
from app import engine
# from app import app
from app import api

from log.logger import logger


@api.route('/main', methods=['GET'])
def main_page():
    """Preparing main page with or without same requests"""
    args = request.args
    logger.info('Get main is work!')

    try:
        with Session(engine) as session:
            data_finish_search = datetime.today().strftime('%Y-%m-%d')
            data_start_search = '2016-01-01'
            fulfilled = str('False')
            if 'data_start' in args:
                data_start_search = args['data_start']
            if 'data_finish' in args:
                data_finish_search = args['data_finish']
            if 'fulfilled' in args:
                fulfilled = args['fulfilled']
#
            id_client_list, id_model_list = [], []
            if 'phone_client' in args:
                phone_client = args['phone_client']
                stmt = (
                    select(DB_client.id_client)
                    .where(DB_client.phone == phone_client)
                    .order_by(DB_client.id_client))
                id_client_list.append(session.execute(stmt).scalar())
            elif 'id_client' in args:
                id_client = args['id_client']
                stmt = (
                    select(DB_client.id_client)
                    .where(DB_client.id_client == id_client)
                    .order_by(DB_client.id_client))
                id_client_list.append(session.execute(stmt).scalar())
            elif 'team' in args:
                team = args['team']
                stmt = (
                    select(DB_client.id_client)
                    .where(DB_client.team == team)
                    .order_by(DB_client.id_client))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
            elif 'coach' in args:
                coach = args['coach']
                stmt = (
                    select(DB_client.id_client)
                    .where(DB_client.coach == coach)
                    .order_by(DB_client.id_client))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
            elif 'city' in args:
                city = args['city']
                stmt = (
                    select(DB_client.id_client)
                    .where(DB_client.sity == city)
                    .order_by(DB_client.id_client))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
#
            if 'kod_model' in args:
                kod_model = args['kod_model']
                stmt = (select(DB_product.id_model)
                    .where(DB_product.kod_model == kod_model)
                    .order_by(DB_product.id_model))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
            elif 'kod_model_like' in args:
                kod_model_like = args['kod_model_like']
                look_for_similar = ('%' + str(kod_model_like) + '%')
                stmt = (
                    select(DB_product.id_model)
                    .where(DB_product.kod_model.ilike(look_for_similar))
                    .order_by(DB_product.id_model))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
            elif 'kolor_model_like' in args:
                kolor_model_like = args['kolor_model_like']
                look_for_similar = ('%' + str(kolor_model_like) + '%')
                stmt = (
                    select(DB_product.id_model)
                    .where(DB_product.kolor_model.ilike(look_for_similar))
                    .order_by(DB_product.id_model))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
# ###########################################################################
            id_order_list = []
            for id_model_cucle in id_model_list:
                stmt = (
                    select(DB_orders.id_order)
                    .where(DB_orders.id_model.any(id_model_cucle)))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_order_list.append(row)
# ###########################################################################
            stmt = (
                select(
                    DB_product.id_model,
                    DB_product.kod_model,
                    DB_product.kolor_model,
                    DB_product.comment_model)
                .order_by(DB_product.id_model))
            data_models = {}
            models = session.execute(stmt).all()
            for model in models:
                data_models.update({
                    model.id_model: [model.kod_model, model.kolor_model, model.comment_model]
                })
# ###########################################################################
            client_alias = aliased(DB_client)
            recipient_alias = aliased(DB_client)
               
            select_modul = (select(
                func.sum(DB_payment.payment).label('my_sum'),
                DB_orders.id_order,
                DB_orders.comment_order,
                DB_orders.data_order,
                DB_orders.data_plane_order,
                DB_orders.fulfilled_order,
                DB_orders.sum_payment,
                DB_orders.discont_order,
                DB_orders.quantity_pars_model,
                DB_orders.phase_1,
                DB_orders.phase_2,
                DB_orders.phase_3,
                DB_orders.id_model,
                client_alias.phone_client.label('phone_order'),
                recipient_alias.second_name_client,
                recipient_alias.first_name_client,
                recipient_alias.phone_client,
                recipient_alias.np_number,
                recipient_alias.zip_code,
                recipient_alias.street_house_apartment,
                recipient_alias.sity)
                .group_by(
                    DB_orders,
                    client_alias,
                    recipient_alias)
                .join(client_alias, DB_orders.id_client == client_alias.id_client)
                .join(recipient_alias, DB_orders.id_recipient == recipient_alias.id_client)
                .outerjoin(DB_payment, DB_orders.id_order == DB_payment.id_order))

            select_modul = select_modul.where(
                                DB_orders.data_order >= data_start_search,
                                DB_orders.data_order <= data_finish_search)

            if fulfilled == 'all':
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        or_(
                            DB_orders.id_client.in_(id_client_list),
                            DB_orders.id_recipient.in_(id_client_list)))\
                        .order_by(DB_orders.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                       DB_orders.id_order.in_(id_order_list))\
                        .order_by(DB_orders.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        and_(
                            DB_orders.id_order.in_(id_order_list),
                            or_(
                                DB_orders.id_client.in_(id_client_list),
                                DB_orders.id_recipient.in_(id_client_list))))\
                        .order_by(DB_orders.id_order)
                else:
                    stmt = select_modul.order_by(DB_orders.id_order)
            else:
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        DB_orders.fulfilled_order == fulfilled,
                        or_(
                            DB_orders.id_client.in_(id_client_list),
                            DB_orders.id_recipient.in_(id_client_list)))\
                        .order_by(DB_orders.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                        DB_orders.fulfilled_order == fulfilled,
                        DB_orders.id_order.in_(id_order_list))\
                        .order_by(DB_orders.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        DB_orders.fulfilled_order == fulfilled,
                        and_(
                            DB_orders.id_order.in_(id_order_list),
                            or_(
                                DB_orders.id_client.in_(id_client_list),
                                DB_orders.id_recipient.in_(id_client_list))))\
                        .order_by(DB_orders.id_order)
                else:
                    if fulfilled == 'true':
                        stmt = select_modul.where(
                            DB_orders.fulfilled_order == fulfilled)\
                            .order_by(DB_orders.id_order)
                    else:
                        stmt = (select_modul
                            .where(DB_orders.fulfilled_order == fulfilled)
                            .order_by(DB_orders.data_plane_order))

            list_order = session.execute(stmt).all()
            # print(list_order)

            if not list_order:
                stmt = select(func.max(DB_orders.id_order))
                last_order = session.execute(stmt).scalar_one()
                stmt = select_modul.where(DB_orders.id_order == last_order)
                list_order = session.execute(stmt).all()
#
            full_block = []
            for row in list_order:
                id_order = row.id_order
                # print(id_order)
                comment_order = row.comment_order
                data_order = (str(row.data_order))
                data_plane_order = (str(row.data_plane_order))
                fulfilled_order = (row.fulfilled_order)
                sum_payment = (row.sum_payment - row.discont_order)
                quantity_pars_model = (row.quantity_pars_model)
                phase_1 = row.phase_1
                phase_2 = row.phase_2
                phase_3 = row.phase_3
                id_models = row.id_model
                phone_client = row.phone_order
                second_name_client = row.second_name_client
                first_name_client = row.first_name_client
                phone_recipient = row.phone_client
                np_number = row.np_number
                zip_code = row.zip_code
                street_house_apartment = row.street_house_apartment
                sity = row.sity
                real_money = row.my_sum
#
                kolor_model, kod_model, comment_model, = [], [], []

                for model in id_models:
                    kod_model.append(data_models.get(model)[0])
                    kolor_model.append(data_models.get(model)[1])
                    comment_model.append(data_models.get(model)[2])

                if len(list(quantity_pars_model)) == 1:
                    quantity_pars_model = quantity_pars_model[0]
                    phase_1 = phase_1[0]
                    phase_2 = phase_2[0]
                    phase_3 = phase_3[0]
                    kolor_model = kolor_model[0]
                    kod_model = kod_model[0]
                    comment_model = comment_model[0]
#
                one_block = {
                    "id_order": id_order,
                    "comment_order": comment_order,
                    "data_order": data_order,
                    "kolor_model": kolor_model,
                    "kod_model": kod_model,
                    "comment_model": comment_model,
                    "quantity_pars_model": quantity_pars_model,
                    "phase_1": phase_1,
                    "phase_2": phase_2,
                    "phase_3": phase_3,
                    "sum_payment": sum_payment,
                    "real_money": real_money,
                    "phone_client": phone_client,
                    "phone_recipient": phone_recipient,
                    "sity": sity,
                    "data_plane_order": data_plane_order,
                    "fulfilled_order": fulfilled_order,
                    "np_number": np_number,
                    "zip_code": zip_code,
                    "street_house_apartment": street_house_apartment,
                    "second_name_client": second_name_client,
                    "first_name_client": first_name_client
                    }
                full_block.append(one_block)
        return jsonify(full_block), 200
    except Exception as e:
        return jsonify(f'Error in function main: {e}')
