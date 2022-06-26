from _2_new_order_page import return_data_from_order_page
from _2_new_order_page import return_data_from_client
from _2_new_order_page import return_data_from_kod
from _2_new_order_page import return_data_from_full_kod
from _2_new_order_page import return_data_from_full_person
from _2_new_order_page import return_data_from_final_order
from _2_new_order_page import return_data_from_edit_order
import json
from sqlalchemy.orm import sessionmaker, session
from data_pompom_create import directory_of_order, directory_of_client
from data_pompom_create import directory_of_color, directory_of_model
from data_pompom_create import engine

Session = sessionmaker(engine)
Session.configure(bind=engine)
session = Session()


def return_data_from_new_order():
    data = return_data_from_order_page()
    id_new_order = data['id_new_order']
    time_last_order = data['time_last_order']
    data_comeback = {
        'id_new_order': id_new_order, 'time_last_order': time_last_order}
    # return data_comeback
    return json.dumps(data_comeback, ensure_ascii=False)
    # return {'id_new_order':id_new_order, 'time_last_order':time_last_order}

# barrier #####################################################################


def return_data_from_new_order_post(data_from_new_page):
    if 'id_order' in data_from_new_page:
        data_new_page = return_data_from_final_order(data_from_new_page)

#############################################################################
    elif 'ur_phone' in data_from_new_page:
        search_data = data_from_new_page['ur_phone']
        w206w = ('%' + str(search_data) + '%')
        ur_phone_1 = session.query(directory_of_client).filter(
            directory_of_client.phone_client.ilike(w206w)).all()
        data_var, id_var = [], []
        for row in ur_phone_1:
            data_var.append(int(row.phone_client))
            id_var.append(row.id_client)
        data_new_page = {"phone_client": data_var, "id_client": id_var}
########
    elif 'ur_second_name' in data_from_new_page:
        search_data = data_from_new_page['ur_second_name']
        w206w = ('%' + str(search_data) + '%')
        ur_second_name_1 = session.query(directory_of_client).filter(
            directory_of_client.second_name_client.ilike(w206w)).all()
        data_var, id_var = [], []
        for row in ur_second_name_1:
            data_var.append(row.second_name_client)
            id_var.append(row.id_client)
        data_new_page = {"second_name_client": data_var, "id_client": id_var}
########
    elif 'ur_team' in data_from_new_page:
        search_data = data_from_new_page['ur_team']
        w206w = ('%' + str(search_data) + '%')
        ur_team_1 = session.query(directory_of_client).filter(
            directory_of_client.team.ilike(w206w)).all()
        data_var = []
        for row in ur_team_1:
            if row.team not in data_var:
                data_var.append(row.team)
        data_new_page = {"name_team": data_var}
########
    elif 'ur_sity' in data_from_new_page:
        search_data = data_from_new_page['ur_sity']
        w206w = ('%' + str(search_data) + '%')
        ur_sity_1 = session.query(directory_of_client).filter(
            directory_of_client.sity.ilike(w206w)).all()
        data_var = []
        for row in ur_sity_1:
            if row.sity not in data_var:
                data_var.append(row.sity)
        data_new_page = {"sity": data_var}
########
    elif 'ur_kolor' in data_from_new_page:
        search_data = data_from_new_page['ur_kolor']
        # w206w=("%"+str(lower(search_data))+"%")
        # print(w206w)
        # print(f'%{search_data}%')
        ur_kolor_1 = session.query(directory_of_color).filter(
            directory_of_color.name_color.ilike(f'%{search_data}%')
            ).order_by('name_color').all()
        full_block = []
        for row in ur_kolor_1:
            data_var = row.name_color
            id_var = row.id_color
            one_block = {"name_color": data_var, "id_color": id_var}
            full_block.append(one_block)
        data_new_page = full_block
########
    elif 'ur_kod' in data_from_new_page:
        search_data = data_from_new_page['ur_kod']
        w206w = ('%' + str(search_data) + '%')
        ur_kod_1 = session.query(directory_of_model).filter(
            directory_of_model.kod_model.ilike(w206w)).order_by(
                'kod_model').all()
        data_var = []
        for row in ur_kod_1:
            data_var.append(row.kod_model)
        data_new_page = {"kod_model": data_var}
# barrier #####################################################################
    elif 'sl_phone' in data_from_new_page:
        search_data = data_from_new_page['sl_phone']
        data_new_page = return_data_from_client(search_data, 0, 0)
####
    elif 'sl_second_name' in data_from_new_page:
        search_data = data_from_new_page['sl_second_name']
        data_new_page = return_data_from_client(0, search_data, 0)
####
    elif 'open_id_client' in data_from_new_page:
        search_data = data_from_new_page['open_id_client']
        data_new_page = return_data_from_client(0, 0, search_data)
####
    elif 'sl_kod' in data_from_new_page:
        search_data = data_from_new_page['sl_kod']
        data_new_page = return_data_from_kod(search_data, 0)
####
    elif 'open_id_model' in data_from_new_page:
        search_data = data_from_new_page['open_id_model']
        data_new_page = return_data_from_kod(0, search_data)
# barrier #####################################################################
    elif 'sl_id_recipient' in data_from_new_page:
        data_tmp_page = return_data_from_full_person(data_from_new_page)
        if 'id_client' in data_tmp_page:
            w1w = data_tmp_page['id_client']
            data_new_page = {"id_recipient": w1w}
        else:
            data_new_page = data_tmp_page
####
    elif 'sl_id_client' in data_from_new_page:
        data_new_page = return_data_from_full_person(data_from_new_page)
####
    elif 'sl_id_model' in data_from_new_page:
        # search_data=data_from_new_page['sl_kod']
        data_new_page = return_data_from_full_kod(data_from_new_page)
####
    elif 'fulfilled_id_order' in data_from_new_page:
        id_order = data_from_new_page['fulfilled_id_order']
        fulfilled_order = data_from_new_page['fulfilled_order']
        rows = session.query(directory_of_order).filter_by(
            id_order=id_order).update({'fulfilled_order': fulfilled_order})
        session.commit()
        data_new_page = {"id_order": "ok"}
# barrier #####################################################################
    elif 'edit_order' in data_from_new_page:
        data_new_page = return_data_from_edit_order(data_from_new_page)

# barrier #####################################################################
    else:
        data_new_page = {"this POST is not correctly"}
    return json.dumps(data_new_page, ensure_ascii=False)
