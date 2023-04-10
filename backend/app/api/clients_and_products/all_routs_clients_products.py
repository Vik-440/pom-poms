"""all routs for clients and pruducts - need refactoring in future!"""

from datetime import datetime, timedelta
import calendar
from flask import jsonify, request
from sqlalchemy import func, select, update#
from sqlalchemy.orm import Session, aliased

from app.clients.models import DB_client
from app.products.models import DB_product
from app.materials.models import DB_materials
from app.payments.models import DB_payment
from app.orders.models import DB_orders
from app import engine
from .. import api
from log.logger import logger


def return_data_from_new_order_post(data_from_new_page):
    with Session(engine) as session:
        if 'id_order' in data_from_new_page:
            data_new_page = return_data_from_final_order(data_from_new_page)
        elif 'ur_phone' in data_from_new_page:
            search_data = data_from_new_page['ur_phone']
            w206w = ('%' + str(search_data) + '%')
            ur_phone_1 = session.query(DB_client).filter(
                DB_client.phone.ilike(w206w)).all()
            data_var, id_var = [], []
            for row in ur_phone_1:
                data_var.append(int(row.phone))
                id_var.append(row.id_client)
            data_new_page = {"phone_client": data_var, "id_client": id_var}
        elif 'ur_second_name' in data_from_new_page:
            search_data = data_from_new_page['ur_second_name']
            w206w = ('%' + str(search_data) + '%')
            ur_second_name_1 = session.query(DB_client).filter(
                DB_client.second_name.ilike(w206w)).all()
            data_var, id_var = [], []
            for row in ur_second_name_1:
                # changed block in 'ur' comands
                second_name_client = row.second_name
                first_name_client = row.first_name
                answer_name = str(second_name_client + ' ' + first_name_client)
                data_var.append(answer_name)
# before I answered only clear 'second_name_client'
                id_var.append(row.id_client)
            data_new_page = {"second_name_client": data_var,
                             "id_client": id_var}
        elif 'ur_team' in data_from_new_page:
            search_data = data_from_new_page['ur_team']
            w206w = ('%' + str(search_data) + '%')
            ur_team_1 = session.query(DB_client).filter(
                DB_client.team.ilike(w206w)).all()
            data_var = []
            for row in ur_team_1:
                if row.team not in data_var:
                    data_var.append(row.team)
            data_new_page = {"name_team": data_var}
        elif 'ur_sity' in data_from_new_page:
            search_data = data_from_new_page['ur_sity']
            w206w = ('%' + str(search_data) + '%')
            ur_sity_1 = session.query(DB_client).filter(
                DB_client.city.ilike(w206w)).all()
            data_var = []
            for row in ur_sity_1:
                if row.city not in data_var:
                    data_var.append(row.city)
            data_new_page = {"sity": data_var}
        elif 'ur_kolor' in data_from_new_page:
            search_data = data_from_new_page['ur_kolor']
            ur_kolor_1 = session.query(DB_materials).filter(
                DB_materials.name.ilike(f'%{search_data}%')
                ).order_by('name_color').all()
            full_block = []
            for row in ur_kolor_1:
                data_var = row.name
                id_var = row.id_material
                one_block = {"name_color": data_var, "id_color": id_var}
                full_block.append(one_block)
            data_new_page = full_block
        elif 'ur_kod' in data_from_new_page:
            search_data = data_from_new_page['ur_kod']
            w206w = ('%' + str(search_data) + '%')
            ur_kod_1 = session.query(DB_product).filter(
                DB_product.article.ilike(w206w)).order_by(
                    'kod_model').all()
            data_var = []
            for row in ur_kod_1:
                data_var.append(row.article)
            data_new_page = {"kod_model": data_var}
        elif 'ur_coach' in data_from_new_page:
            search_data = data_from_new_page['ur_coach']
            w206w = ('%' + str(search_data) + '%')
            ur_coach_1 = session.query(DB_client).filter(
                DB_client.coach.ilike(w206w)).all()
            data_var = []
            for row in ur_coach_1:
                data_var.append(row.coach)
            data_new_page = {"coach": data_var}
        elif 'sl_phone' in data_from_new_page:
            search_data = data_from_new_page['sl_phone']
            data_new_page = return_data_from_client(search_data, 0, 0)
        elif 'sl_second_name' in data_from_new_page:
            search_data = data_from_new_page['sl_second_name']
            data_new_page = return_data_from_client(0, search_data, 0)
        elif 'open_id_client' in data_from_new_page:
            search_data = data_from_new_page['open_id_client']
            data_new_page = return_data_from_client(0, 0, search_data)
        elif 'sl_kod' in data_from_new_page:
            search_data = data_from_new_page['sl_kod']
            data_new_page = return_data_from_kod(search_data, 0)
        elif 'open_id_model' in data_from_new_page:
            search_data = data_from_new_page['open_id_model']
            data_new_page = return_data_from_kod(0, search_data)
        elif 'sl_id_recipient' in data_from_new_page:
            data_tmp_page = return_data_from_full_person(data_from_new_page)
            if 'id_client' in data_tmp_page:
                w1w = data_tmp_page['id_client']
                data_new_page = {"id_recipient": w1w}
            else:
                data_new_page = data_tmp_page
        elif 'sl_id_client' in data_from_new_page:
            data_new_page = return_data_from_full_person(data_from_new_page)
        elif 'sl_id_model' in data_from_new_page:
            # search_data=data_from_new_page['sl_kod']
            data_new_page = return_data_from_full_kod(data_from_new_page)
        elif 'fulfilled_id_order' in data_from_new_page:
            id_order = data_from_new_page['fulfilled_id_order']
            fulfilled_order = data_from_new_page['fulfilled_order']
            session.query(DB_orders).filter_by(
                id_order=id_order).update({'status_order': fulfilled_order})
            data_new_page = {"id_order": "ok"}
        elif 'edit_order' in data_from_new_page:
            data_new_page = return_data_from_edit_order(data_from_new_page)
        else:
            data_new_page = {"this POST is not correctly"}
        session.commit()
        return data_new_page


def return_data_from_client(sl_phone, sl_second_name, open_id_client):
    with Session(engine) as session:
        if sl_phone == 0 and open_id_client == 0:
            id_client_3 = session.query(DB_client).filter_by(
                second_name=sl_second_name).all()
        elif sl_second_name == 0 and open_id_client == 0:
            sl_phone = str(sl_phone)
            id_client_3 = session.query(DB_client).filter_by(
                phone=str(sl_phone)).all()
        else:
            id_client_3 = session.query(DB_client).filter_by(
                id_client=open_id_client).all()
        for row in id_client_3:
            j_id_client = row.id_client
            j_sity = row.city
            j_name_team = row.team
        phone_client_1 = session.query(DB_client).filter_by(
            id_client=j_id_client).all()

        for row1 in phone_client_1:
            j_phone_client = (row1.phone)
            j_second_name_client = (row1.second_name)
            j_first_name_client = (row1.first_name)
            j_surname_client = (row1.surname)
            j_np_number = (row1.np_number)
            j_coach = (row1.coach)
            j_zip_code = (row1.zip_code)
            j_street_house_apartment = (row1.address)
            j_comment_client = (row1.comment)

        one_block = {"id_client": j_id_client, "phone_client": j_phone_client,
                     "second_name_client": j_second_name_client,
                     "first_name_client": j_first_name_client,
                     "surname_client": j_surname_client, "sity": j_sity,
                     "np_number": j_np_number, "name_team": j_name_team,
                     "coach": j_coach, "zip_code": j_zip_code,
                     "street_house_apartment": j_street_house_apartment,
                     "comment_client": j_comment_client}
    return one_block


def return_data_from_kod(sl_kod, open_id_model):
    with Session(engine) as session:
        if open_id_model == 0:
            id_model_1 = session.query(DB_product).filter_by(
                article=sl_kod).all()
        else:
            id_model_1 = session.query(DB_product).filter_by(
                id_product=open_id_model).all()
        for row in id_model_1:
            j_id_model = row.id_product
            j_kod_model = row.article
            j_id_color_1 = row.id_color_1
            j_id_color_part_1 = row.part_1
            j_id_color_2 = row.id_color_2
            j_id_color_part_2 = row.part_2
            j_id_color_3 = row.id_color_3
            j_id_color_part_3 = row.part_3
            j_id_color_4 = row.id_color_4
            j_id_color_part_4 = row.part_4
            j_price_model = row.price
            j_comment_model = row.comment
            j_kolor_model = row.colors

        name_color_0 = session.query(DB_materials).filter_by(
            id_material=j_id_color_1).all()
        for row in name_color_0:
            name_color_1 = row.name
        if j_id_color_2 != 0 and j_id_color_2 is not None:
            name_color_0 = session.query(DB_materials).filter_by(
                id_material=j_id_color_2).all()
            for row in name_color_0:
                name_color_2 = row.name
        else:
            name_color_2 = 0
        if j_id_color_3 != 0 and j_id_color_3 is not None:
            name_color_0 = session.query(DB_materials).filter_by(
                id_material=j_id_color_3).all()
            for row in name_color_0:
                name_color_3 = row.name
        else:
            name_color_3 = 0
        if j_id_color_4 != 0 and j_id_color_4 is not None:
            name_color_0 = session.query(DB_materials).filter_by(
                id_material=j_id_color_4).all()
            for row in name_color_0:
                name_color_4 = row.name
        else:
            name_color_4 = 0
        if len(str(id_model_1)) < 3:
            one_block = {}
        else:
            one_block = {"id_model": j_id_model, "kod_model": j_kod_model,
                         "id_color_1": j_id_color_1,
                         "name_color_1": name_color_1,
                         "id_color_part_1": j_id_color_part_1,
                         "id_color_2": j_id_color_2,
                         "name_color_2": name_color_2,
                         "id_color_part_2": j_id_color_part_2,
                         "id_color_3": j_id_color_3,
                         "name_color_3": name_color_3,
                         "id_color_part_3": j_id_color_part_3,
                         "id_color_4": j_id_color_4,
                         "name_color_4": name_color_4,
                         "id_color_part_4": j_id_color_part_4,
                         "price_model": j_price_model,
                         "comment_model": j_comment_model,
                         "kolor_model": j_kolor_model}
    return one_block


def return_data_from_full_kod(data_from_new_page):
    with Session(engine) as session:
        j_id_model = 0
        search_data = data_from_new_page['kod_model']
        id_model_1 = session.query(DB_product).filter_by(
            article=search_data).all()
        for row in id_model_1:
            j_id_model = row.id_product
        if j_id_model == 0:
            ins = DB_product(
                article=data_from_new_page['kod_model'],    # int for all
                id_color_1=int(data_from_new_page['id_color_1']),
                part_1=int(data_from_new_page['id_color_part_1']),
                id_color_2=int(data_from_new_page['id_color_2']),
                part_2=int(data_from_new_page['id_color_part_2']),
                id_color_3=int(data_from_new_page['id_color_3']),
                part_3=int(data_from_new_page['id_color_part_3']),
                id_color_4=int(data_from_new_page['id_color_4']),
                part_4=int(data_from_new_page['id_color_part_4']),
                price=data_from_new_page['price_model'],
                comment=data_from_new_page['comment_model'],
                colors=data_from_new_page['kolor_model'])
            session.add(ins)
            session.commit()

            id_model_1 = session.query(DB_product).filter_by(
                article=search_data).all()
            for row in id_model_1:
                j_id_model = row.id_product
            one_block = {"id_model": j_id_model}
        else:
            ins = session.query(DB_product).filter(
                DB_product.id_product == j_id_model).update(
                    {'article': data_from_new_page['kod_model'],
                        'id_color_1': int(data_from_new_page['id_color_1']),
                        'part_1': int(
                        data_from_new_page['id_color_part_1']),
                        'id_color_2': int(data_from_new_page['id_color_2']),
                        'part_2': int(
                            data_from_new_page['id_color_part_2']),
                        'id_color_3': int(data_from_new_page['id_color_3']),
                        'part_3': int(
                            data_from_new_page['id_color_part_3']),
                        'id_color_4': int(data_from_new_page['id_color_4']),
                        'part_4': int(
                            data_from_new_page['id_color_part_4']),
                        'price': data_from_new_page['price_model'],
                        'comment': data_from_new_page['comment_model'],
                        'colors': data_from_new_page['kolor_model']})
            session.commit()

            # q1q = ('id_model=' + str(j_id_model) + ' is updated')
            one_block = {"id_model": j_id_model}
        return one_block


def return_data_from_full_person(data_from_new_page):
    with Session(engine) as session:
        j_second_name_client = 0
        search_data = str(data_from_new_page['phone_client'])
        second_name_client_1 = session.query(DB_client).filter_by(
            phone=search_data).all()
        for row in second_name_client_1:
            j_second_name_client = row.second_name
            tmp_id_client = row.id_client

        second_name_client = data_from_new_page[
            'second_name_client'].capitalize()
        first_name_client = data_from_new_page[
            'first_name_client'].capitalize()
        surname_client = data_from_new_page[
            'surname_client']
        if surname_client:
            surname_client = surname_client.capitalize()
        city = data_from_new_page['sity']
        if city:
            city = city.capitalize()
        team = data_from_new_page['name_team']
        if team:
            team = team.capitalize()
        coach = data_from_new_page['coach']
        if coach:
            coach = coach.capitalize()

        if j_second_name_client == 0:
            ins = DB_client(
                phone=data_from_new_page['phone_client'],
                second_name=second_name_client,
                first_name=first_name_client,
                surname=surname_client,
                city=city,
                np_number=data_from_new_page['np_number'],
                team=team,
                coach=coach,
                zip_code=data_from_new_page['zip_code'],
                address=data_from_new_page[
                    'street_house_apartment'],
                comment=data_from_new_page['comment_client'])
            session.add(ins)
            session.commit()

            id_client_1 = session.query(DB_client).filter_by(
                phone=search_data).all()
            for row in id_client_1:
                j_id_client = row.id_client
            one_block = {"id_client": j_id_client}
        else:
            ins = session.query(DB_client).filter(
                DB_client.id_client == tmp_id_client).update(
                    {'phone': data_from_new_page['phone_client'],
                        'second_name': second_name_client,
                        'first_name': first_name_client,
                        'surname': surname_client,
                        'city': city,
                        'np_number': data_from_new_page['np_number'],
                        'team': team,
                        'coach': coach,
                        'zip_code': data_from_new_page['zip_code'],
                        'address': data_from_new_page[
                            'street_house_apartment'],
                        'comment': data_from_new_page['comment_client']}
            )
            session.commit()
            q1q = ('updated id_client - ' + str(tmp_id_client))
            one_block = {"phone_client": q1q}
        return one_block


def return_data_from_final_order(data_from_new_page):
    with Session(engine) as session:
        e = "Error in real recipient number"
        id_client = data_from_new_page['id_client']
        if id_client is None:
            return f'Error in client number: {e}', 500
        check_client = session.query(DB_client).filter_by(
            id_client=id_client).scalar()
        if check_client is None:
            raise Exception("Error in real client number ")
        id_recipient = data_from_new_page['id_recipient']
        if id_recipient is None:
            return f'Error in recipient number: {e}', 500
        check_client = session.query(DB_client).filter_by(
            id_client=id_recipient).scalar()
        if check_client is None:
            raise Exception("Error in real recipient number ")
        if data_from_new_page['quantity_pars_model'] is None:
            raise Exception("Error: quantity_pars is empty")
        id_order = int(data_from_new_page['id_order'])
        check_order = session.query(DB_orders).filter_by(
            id_order=id_order).scalar()

        # s2s = len((data_from_new_page['id_model']))
        # phase_pcs = []
        # while s2s > 0:
        #     s2s -= 1
        #     phase_pcs.append(False)
        phase_int, phase_int3 = [], []
        for y in data_from_new_page['quantity_pars_model']:
            phase_int.append(y * 2)
            phase_int3.append(y)
        if 'edit_real_order' in data_from_new_page:
            # print("problems")
            x1x = int(data_from_new_page['edit_real_order'])
            if x1x != id_order:
                raise Exception("This order number is real - 1p")
            # print(data_from_new_page)
            session.query(DB_orders).filter(
                DB_orders.id_order == id_order).update(
                {"id_order": id_order,
                    "date_create": data_from_new_page['data_order'],
                    "id_client": data_from_new_page['id_client'],
                    "id_recipient": data_from_new_page['id_recipient'],
                    "date_plane_send": data_from_new_page['data_plane_order'],
                    # "data_send_order": data_from_new_page['data_send_order'],
                    "discount": data_from_new_page['discont_order'],
                    "sum_payment": data_from_new_page['sum_payment'],
                    "status_order": data_from_new_page['fulfilled_order'],
                    "comment": data_from_new_page['comment_order'],
                    # test changing
                    "phase_1": data_from_new_page['phase_1'],
                    "phase_2": data_from_new_page['phase_2'],
                    "phase_3": data_from_new_page['phase_3'],
                    # test changing finish
                    "id_models": data_from_new_page['id_model'],
                    "qty_pars": data_from_new_page[
                        'quantity_pars_model'],
                    "price_model_sell": data_from_new_page[
                        'price_model_order']})
            session.commit()
            one_block = {"edit_real_order": x1x}
            return one_block
        



        # print(data_from_new_page)
        if check_order is not None and id_order != 0:
            raise Exception("This order number is real - 2p")
        if id_order == 0:
            id_order_max = session.query(func.max(
                DB_orders.id_order)).first()
            id_order = int(id_order_max[0]) + 1

        ins = DB_orders(
            id_order=id_order,
            date_create=data_from_new_page['data_order'],
            id_client=data_from_new_page['id_client'],
            id_recipient=data_from_new_page['id_recipient'],
            date_plane_send=data_from_new_page['data_plane_order'],
            # data_send_order=data_from_new_page['data_send_order'],
            discount=data_from_new_page['discont_order'],
            sum_payment=data_from_new_page['sum_payment'],
            status_order=data_from_new_page['fulfilled_order'],
            comment=data_from_new_page['comment_order'],
            # test changing
            phase_1=data_from_new_page['phase_1'],
            phase_2=data_from_new_page['phase_2'],
            phase_3=data_from_new_page['phase_3'],
            # phase_1=phase_int,
            # phase_2=phase_int,
            # phase_3=phase_int3,
            # test changing finish
            id_models=data_from_new_page['id_model'],
            qty_pars=data_from_new_page['quantity_pars_model'],
            price_model_sell=data_from_new_page['price_model_order'])
        session.add(ins)
        session.commit()
        session.refresh(ins)
        j_id_order = ins.id_order

        one_block = {"id_order": j_id_order}
    return one_block


def return_data_from_edit_order(data_from_new_page):
    with Session(engine) as session:
        edit_order = data_from_new_page['edit_order']
        id_order_1 = session.query(DB_orders).filter_by(
            id_order=edit_order).all()
        for row in id_order_1:
            id_order = row.id_order
            data_order = str(row.date_create)
            id_client = row.id_client
            id_recipient = row.id_recipient
            data_plane_order = str(row.date_plane_send)
            # data_send_order = str(row.data_plane_order)
            discont_order = row.discount
            sum_payment = row.sum_payment
            fulfilled_order = row.status_order
            comment_order = row.comment
            id_model = (row.id_models)
            quantity_pars_model = (row.qty_pars)
            price_model_order = (row.price_model_sell)
            phase_1 = row.phase_1
            phase_2 = row.phase_2
            phase_3 = row.phase_3

            real_money_order_1 = session.query(
                func.sum(DB_payment.payment).label(
                    'sum_order')).filter_by(
                id_order=id_order).first()
            for row in real_money_order_1:
                real_money_order = real_money_order_1.sum_order

        if len(str(id_order_1)) < 3:
            one_block = {}
        else:
            one_block = {"id_order": id_order, "data_order": data_order,
                         "id_client": id_client, "id_recipient": id_recipient,
                         "data_plane_order": data_plane_order,
                         #  "data_send_order": data_plane_order,   # delete
                         "discont_order": discont_order,
                         "sum_payment": sum_payment,
                         "fulfilled_order": fulfilled_order,
                         "comment_order": comment_order, "id_model": id_model,
                         "quantity_pars_model": quantity_pars_model,
                         "price_model_order": price_model_order,
                         "real_money_order": real_money_order,
                         "phase_1": phase_1, "phase_2": phase_2,
                         "phase_3": phase_3}
    return one_block



@api.route('/new_order', methods=['POST'])
def clients_products_orders():
    try:
            data = request.get_json()
            return jsonify(return_data_from_new_order_post(data)), 200
    except Exception as e:
        logger.error(f'Error in function new_order: {e}')
        return f'Error in function new_order: {e}', 500
    