import json
from sqlalchemy.orm import Session
from db.models import engine

from functions.orders.new_order_page import (
    return_data_from_order_page,
    return_data_from_client,
    return_data_from_kod,
    return_data_from_full_kod,
    return_data_from_full_person,
    return_data_from_final_order,
    return_data_from_edit_order)
from db.models import (
    directory_of_order as db_o,
    directory_of_client as db_c,
    directory_of_color as db_col,
    directory_of_model as db_m)


def return_data_from_new_order():
    data = return_data_from_order_page()
    id_new_order = data['id_new_order']
    time_last_order = data['time_last_order']
    data_comeback = {
        'id_new_order': id_new_order, 'time_last_order': time_last_order}
    # return data_comeback
    return json.dumps(data_comeback, ensure_ascii=False)
    # return {'id_new_order':id_new_order, 'time_last_order':time_last_order}


def return_data_from_new_order_post(data_from_new_page):
    with Session(engine) as session:
        if 'id_order' in data_from_new_page:
            data_new_page = return_data_from_final_order(data_from_new_page)
        elif 'ur_phone' in data_from_new_page:
            search_data = data_from_new_page['ur_phone']
            w206w = ('%' + str(search_data) + '%')
            ur_phone_1 = session.query(db_c).filter(
                db_c.phone_client.ilike(w206w)).all()
            data_var, id_var = [], []
            for row in ur_phone_1:
                data_var.append(int(row.phone_client))
                id_var.append(row.id_client)
            data_new_page = {"phone_client": data_var, "id_client": id_var}
        elif 'ur_second_name' in data_from_new_page:
            search_data = data_from_new_page['ur_second_name']
            w206w = ('%' + str(search_data) + '%')
            ur_second_name_1 = session.query(db_c).filter(
                db_c.second_name_client.ilike(w206w)).all()
            data_var, id_var = [], []
            for row in ur_second_name_1:
                # changed block in 'ur' comands
                second_name_client = row.second_name_client
                first_name_client = row.first_name_client
                answer_name = str(second_name_client + ' ' + first_name_client)
                data_var.append(answer_name)
# before I answered only clear 'second_name_client'
                id_var.append(row.id_client)
            data_new_page = {"second_name_client": data_var,
                             "id_client": id_var}
        elif 'ur_team' in data_from_new_page:
            search_data = data_from_new_page['ur_team']
            w206w = ('%' + str(search_data) + '%')
            ur_team_1 = session.query(db_c).filter(
                db_c.team.ilike(w206w)).all()
            data_var = []
            for row in ur_team_1:
                if row.team not in data_var:
                    data_var.append(row.team)
            data_new_page = {"name_team": data_var}
        elif 'ur_sity' in data_from_new_page:
            search_data = data_from_new_page['ur_sity']
            w206w = ('%' + str(search_data) + '%')
            ur_sity_1 = session.query(db_c).filter(
                db_c.sity.ilike(w206w)).all()
            data_var = []
            for row in ur_sity_1:
                if row.sity not in data_var:
                    data_var.append(row.sity)
            data_new_page = {"sity": data_var}
        elif 'ur_kolor' in data_from_new_page:
            search_data = data_from_new_page['ur_kolor']
            ur_kolor_1 = session.query(db_col).filter(
                db_col.name_color.ilike(f'%{search_data}%')
                ).order_by('name_color').all()
            full_block = []
            for row in ur_kolor_1:
                data_var = row.name_color
                id_var = row.id_color
                one_block = {"name_color": data_var, "id_color": id_var}
                full_block.append(one_block)
            data_new_page = full_block
        elif 'ur_kod' in data_from_new_page:
            search_data = data_from_new_page['ur_kod']
            w206w = ('%' + str(search_data) + '%')
            ur_kod_1 = session.query(db_m).filter(
                db_m.kod_model.ilike(w206w)).order_by(
                    'kod_model').all()
            data_var = []
            for row in ur_kod_1:
                data_var.append(row.kod_model)
            data_new_page = {"kod_model": data_var}
        elif 'ur_coach' in data_from_new_page:
            search_data = data_from_new_page['ur_coach']
            w206w = ('%' + str(search_data) + '%')
            ur_coach_1 = session.query(db_c).filter(
                db_c.coach.ilike(w206w)).all()
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
            session.query(db_o).filter_by(
                id_order=id_order).update({'fulfilled_order': fulfilled_order})
            data_new_page = {"id_order": "ok"}
        elif 'edit_order' in data_from_new_page:
            data_new_page = return_data_from_edit_order(data_from_new_page)
        else:
            data_new_page = {"this POST is not correctly"}
        session.commit()
        return json.dumps(data_new_page, ensure_ascii=False)
