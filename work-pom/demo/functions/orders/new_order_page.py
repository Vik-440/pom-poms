"""This file waits for refactoring and drops"""
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.models import engine
from db.models import (
    directory_of_order as db_o,
    directory_of_client as db_c,
    directory_of_color as db_col,
    directory_of_model as db_m,
    directory_of_payment as db_p)


def return_data_from_order_page():
    with Session(engine) as session:
        id_new_order = session.query(func.max(db_o.id_order))
        for row222 in id_new_order:
            j_id_new_order = row222[0]+1
        time_last_order = '2022-12-31'
        return {
            'id_new_order': j_id_new_order, 'time_last_order': time_last_order}


def return_data_from_client(sl_phone, sl_second_name, open_id_client):
    with Session(engine) as session:
        if sl_phone == 0 and open_id_client == 0:
            id_client_3 = session.query(db_c).filter_by(
                second_name_client=sl_second_name).all()
        elif sl_second_name == 0 and open_id_client == 0:
            sl_phone = str(sl_phone)
            id_client_3 = session.query(db_c).filter_by(
                phone_client=str(sl_phone)).all()
        else:
            id_client_3 = session.query(db_c).filter_by(
                id_client=open_id_client).all()
        for row in id_client_3:
            j_id_client = row.id_client
            j_sity = row.sity
            j_name_team = row.team
        phone_client_1 = session.query(db_c).filter_by(
            id_client=j_id_client).all()

        for row1 in phone_client_1:
            j_phone_client = (row1.phone_client)
            j_second_name_client = (row1.second_name_client)
            j_first_name_client = (row1.first_name_client)
            j_surname_client = (row1.surname_client)
            j_np_number = (row1.np_number)
            j_coach = (row1.coach)
            j_zip_code = (row1.zip_code)
            j_street_house_apartment = (row1.street_house_apartment)
            j_comment_client = (row1.comment_client)

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
            id_model_1 = session.query(db_m).filter_by(
                kod_model=sl_kod).all()
        else:
            id_model_1 = session.query(db_m).filter_by(
                id_model=open_id_model).all()
        for row in id_model_1:
            j_id_model = row.id_model
            j_kod_model = row.kod_model
            j_id_color_1 = row.id_color_1
            j_id_color_part_1 = row.id_color_part_1
            j_id_color_2 = row.id_color_2
            j_id_color_part_2 = row.id_color_part_2
            j_id_color_3 = row.id_color_3
            j_id_color_part_3 = row.id_color_part_3
            j_id_color_4 = row.id_color_4
            j_id_color_part_4 = row.id_color_part_4
            j_price_model = row.price_model
            j_comment_model = row.comment_model
            j_kolor_model = row.kolor_model

        name_color_0 = session.query(db_col).filter_by(
            id_color=j_id_color_1).all()
        for row in name_color_0:
            name_color_1 = row.name_color
        if j_id_color_2 != 0 and j_id_color_2 is not None:
            name_color_0 = session.query(db_col).filter_by(
                id_color=j_id_color_2).all()
            for row in name_color_0:
                name_color_2 = row.name_color
        else:
            name_color_2 = 0
        if j_id_color_3 != 0 and j_id_color_3 is not None:
            name_color_0 = session.query(db_col).filter_by(
                id_color=j_id_color_3).all()
            for row in name_color_0:
                name_color_3 = row.name_color
        else:
            name_color_3 = 0
        if j_id_color_4 != 0 and j_id_color_4 is not None:
            name_color_0 = session.query(db_col).filter_by(
                id_color=j_id_color_4).all()
            for row in name_color_0:
                name_color_4 = row.name_color
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
        id_model_1 = session.query(db_m).filter_by(
            kod_model=search_data).all()
        for row in id_model_1:
            j_id_model = row.id_model
        if j_id_model == 0:
            ins = db_m(
                    kod_model=data_from_new_page['kod_model'],    # int for all
                    id_color_1=int(data_from_new_page['id_color_1']),
                    id_color_part_1=int(data_from_new_page['id_color_part_1']),
                    id_color_2=int(data_from_new_page['id_color_2']),
                    id_color_part_2=int(data_from_new_page['id_color_part_2']),
                    id_color_3=int(data_from_new_page['id_color_3']),
                    id_color_part_3=int(data_from_new_page['id_color_part_3']),
                    id_color_4=int(data_from_new_page['id_color_4']),
                    id_color_part_4=int(data_from_new_page['id_color_part_4']),
                    price_model=data_from_new_page['price_model'],
                    comment_model=data_from_new_page['comment_model'],
                    kolor_model=data_from_new_page['kolor_model'])
            session.add(ins)
            session.commit()

            id_model_1 = session.query(db_m).filter_by(
                kod_model=search_data).all()
            for row in id_model_1:
                j_id_model = row.id_model
            one_block = {"id_model": j_id_model}
        else:
            ins = session.query(db_m).filter(
                db_m.id_model == j_id_model).update(
                    {'kod_model': data_from_new_page['kod_model'],
                        'id_color_1': int(data_from_new_page['id_color_1']),
                        'id_color_part_1': int(
                        data_from_new_page['id_color_part_1']),
                        'id_color_2': int(data_from_new_page['id_color_2']),
                        'id_color_part_2': int(
                            data_from_new_page['id_color_part_2']),
                        'id_color_3': int(data_from_new_page['id_color_3']),
                        'id_color_part_3': int(
                            data_from_new_page['id_color_part_3']),
                        'id_color_4': int(data_from_new_page['id_color_4']),
                        'id_color_part_4': int(
                            data_from_new_page['id_color_part_4']),
                        'price_model': data_from_new_page['price_model'],
                        'comment_model': data_from_new_page['comment_model'],
                        'kolor_model': data_from_new_page['kolor_model']})
            session.commit()

            # q1q = ('id_model=' + str(j_id_model) + ' is updated')
            one_block = {"id_model": j_id_model}
        return one_block


def return_data_from_full_person(data_from_new_page):
    with Session(engine) as session:
        j_second_name_client = 0
        search_data = str(data_from_new_page['phone_client'])
        second_name_client_1 = session.query(db_c).filter_by(
            phone_client=search_data).all()
        for row in second_name_client_1:
            j_second_name_client = row.second_name_client
            tmp_id_client = row.id_client

        second_name_client = data_from_new_page[
                        'second_name_client'].title()
        first_name_client = data_from_new_page[
                        'first_name_client'].title()
        surname_client = data_from_new_page[
                        'surname_client']
        if surname_client:
            surname_client = surname_client.title()
        sity = data_from_new_page['sity']
        if sity:
            sity = sity.title()
        team = data_from_new_page['name_team']
        if team:
            team = team.title()
        coach = data_from_new_page['coach']
        if coach:
            coach = coach.title()

        if j_second_name_client == 0:
            ins = db_c(
                    phone_client=data_from_new_page['phone_client'],
                    second_name_client=second_name_client,
                    first_name_client=first_name_client,
                    surname_client=surname_client,
                    sity=sity,
                    np_number=data_from_new_page['np_number'],
                    team=team,
                    coach=coach,
                    zip_code=data_from_new_page['zip_code'],
                    street_house_apartment=data_from_new_page[
                        'street_house_apartment'],
                    comment_client=data_from_new_page['comment_client'])
            session.add(ins)
            session.commit()

            id_client_1 = session.query(db_c).filter_by(
                phone_client=search_data).all()
            for row in id_client_1:
                j_id_client = row.id_client
            one_block = {"id_client": j_id_client}
        else:
            ins = session.query(db_c).filter(
                db_c.id_client == tmp_id_client).update(
                    {'phone_client': data_from_new_page['phone_client'],
                        'second_name_client': second_name_client,
                        'first_name_client': first_name_client,
                        'surname_client': surname_client,
                        'sity': sity,
                        'np_number': data_from_new_page['np_number'],
                        'team': team,
                        'coach': coach,
                        'zip_code': data_from_new_page['zip_code'],
                        'street_house_apartment': data_from_new_page[
                            'street_house_apartment'],
                        'comment_client': data_from_new_page['comment_client']}
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
        check_client = session.query(db_c).filter_by(
            id_client=id_client).scalar()
        if check_client is None:
            raise Exception("Error in real client number ")
        id_recipient = data_from_new_page['id_recipient']
        if id_recipient is None:
            return f'Error in recipient number: {e}', 500
        check_client = session.query(db_c).filter_by(
            id_client=id_recipient).scalar()
        if check_client is None:
            raise Exception("Error in real recipient number ")
        if data_from_new_page['quantity_pars_model'] is None:
            raise Exception("Error: quantity_pars is empty")
        id_order = int(data_from_new_page['id_order'])
        check_order = session.query(db_o).filter_by(
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
            session.query(db_o).filter(
                db_o.id_order == id_order).update(
                   {"id_order": id_order,
                    "data_order": data_from_new_page['data_order'],
                    "id_client": data_from_new_page['id_client'],
                    "id_recipient": data_from_new_page['id_recipient'],
                    "data_plane_order": data_from_new_page['data_plane_order'],
                    # "data_send_order": data_from_new_page['data_send_order'],
                    "discont_order": data_from_new_page['discont_order'],
                    "sum_payment": data_from_new_page['sum_payment'],
                    "fulfilled_order": data_from_new_page['fulfilled_order'],
                    "comment_order": data_from_new_page['comment_order'],
                    # test changing
                    "phase_1": data_from_new_page['phase_1'],
                    "phase_2": data_from_new_page['phase_2'],
                    "phase_3": data_from_new_page['phase_3'],
                    # test changing finish
                    "id_model": data_from_new_page['id_model'],
                    "quantity_pars_model": data_from_new_page[
                        'quantity_pars_model'],
                    "price_model_order": data_from_new_page[
                        'price_model_order']})
            session.commit()
            one_block = {"edit_real_order": x1x}
            return one_block

        if check_order is not None and id_order != 0:
            raise Exception("This order number is real - 2p")
        if id_order == 0:
            id_order_max = session.query(func.max(
                db_o.id_order)).first()
            id_order = int(id_order_max[0]) + 1

        ins = db_o(
            id_order=id_order,
            data_order=data_from_new_page['data_order'],
            id_client=data_from_new_page['id_client'],
            id_recipient=data_from_new_page['id_recipient'],
            data_plane_order=data_from_new_page['data_plane_order'],
            # data_send_order=data_from_new_page['data_send_order'],
            discont_order=data_from_new_page['discont_order'],
            sum_payment=data_from_new_page['sum_payment'],
            fulfilled_order=data_from_new_page['fulfilled_order'],
            comment_order=data_from_new_page['comment_order'],
            # test changing
            phase_1=data_from_new_page['phase_1'],
            phase_2=data_from_new_page['phase_2'],
            phase_3=data_from_new_page['phase_3'],
            # phase_1=phase_int,
            # phase_2=phase_int,
            # phase_3=phase_int3,
            # test changing finish
            id_model=data_from_new_page['id_model'],
            quantity_pars_model=data_from_new_page['quantity_pars_model'],
            price_model_order=data_from_new_page['price_model_order'])
        session.add(ins)
        session.commit()
        session.refresh(ins)
        j_id_order = ins.id_order

        one_block = {"id_order": j_id_order}
    return one_block


def return_data_from_edit_order(data_from_new_page):
    with Session(engine) as session:
        edit_order = data_from_new_page['edit_order']
        id_order_1 = session.query(db_o).filter_by(
            id_order=edit_order).all()
        for row in id_order_1:
            id_order = row.id_order
            data_order = str(row.data_order)
            id_client = row.id_client
            id_recipient = row.id_recipient
            data_plane_order = str(row.data_plane_order)
            # data_send_order = str(row.data_plane_order)
            discont_order = row.discont_order
            sum_payment = row.sum_payment
            fulfilled_order = row.fulfilled_order
            comment_order = row.comment_order
            id_model = (row.id_model)
            quantity_pars_model = (row.quantity_pars_model)
            price_model_order = (row.price_model_order)
            phase_1 = row.phase_1
            phase_2 = row.phase_2
            phase_3 = row.phase_3

            real_money_order_1 = session.query(
                func.sum(db_p.payment).label(
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