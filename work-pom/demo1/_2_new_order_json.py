from sqlalchemy import null
from _2_new_order_page import return_data_from_order_page, return_data_from_client, return_data_from_kod
from _2_new_order_page import return_data_from_full_kod, return_data_from_full_person, return_data_from_final_order
import json
from sqlalchemy import create_engine,  MetaData, true, text, Integer, String, Table, Column, and_, or_
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine

# log_pass_sql = 'postgresql+psycopg2://postgres:123123@localhost/postgres'
# engine = create_engine(log_pass_sql)

Session = sessionmaker(engine)
Session.configure(bind=engine)
session = Session()

def return_data_from_new_order():
    data = return_data_from_order_page()
    id_new_order = data['id_new_order']
    time_last_order = data['time_last_order']
    data_comeback= {'id_new_order':id_new_order, 'time_last_order':time_last_order}
    # return data_comeback
    return json.dumps(data_comeback, ensure_ascii=False)
    # return {'id_new_order':id_new_order, 'time_last_order':time_last_order}



#############################################################################
def return_data_from_new_order_post(data_from_new_page):
    if 'id_order' in data_from_new_page:
        data_new_page=return_data_from_final_order(data_from_new_page)
        
#############################################################################
    elif 'ur_phone' in data_from_new_page:
        search_data=data_from_new_page['ur_phone']
        w206w=('%'+ str(search_data) +'%')
        ur_phone_1=session.query(directory_of_client).filter(directory_of_client.phone_client.ilike(w206w)).all()
        data_var=[]
        for row in ur_phone_1:
            data_var.append(int(row.phone_client))
        data_new_page = {"phone_client" : data_var}
########
    elif 'ur_second_name' in data_from_new_page:
        search_data=data_from_new_page['ur_second_name']
        w206w=('%'+ str(search_data) +'%')
        ur_second_name_1=session.query(directory_of_client).filter(directory_of_client.second_name_client.ilike(w206w)).all()
        data_var=[]
        for row in ur_second_name_1:
            data_var.append(row.second_name_client)
        data_new_page = {"second_name_client" : data_var}
########
    elif 'ur_team' in data_from_new_page:
        search_data=data_from_new_page['ur_team']
        w206w=('%'+ str(search_data) +'%')
        ur_team_1=session.query(directory_of_team).filter(directory_of_team.name_team.ilike(w206w)).all()
        data_var=[]
        for row in ur_team_1:
            data_var.append(row.name_team)
        data_new_page = {"name_team" : data_var}
########
    elif 'ur_sity' in data_from_new_page:
        search_data=data_from_new_page['ur_sity']
        w206w=('%'+ str(search_data) +'%')
        ur_sity_1=session.query(directory_of_sity).filter(directory_of_sity.sity.ilike(w206w)).all()
        data_var=[]
        for row in ur_sity_1:
            data_var.append(row.sity)
        data_new_page = {"sity" : data_var}
########
    elif 'ur_kolor' in data_from_new_page:
        search_data=data_from_new_page['ur_kolor']
        w206w=('%'+ str(search_data) +'%')
        ur_kolor_1=session.query(directory_of_color).filter(directory_of_color.name_color.ilike(w206w)).all()
        data_var=[]
        for row in ur_kolor_1:
            data_var.append(row.name_color)
        data_new_page = {"name_color" : data_var}
########
    elif 'ur_kod' in data_from_new_page:
        search_data=data_from_new_page['ur_kod']
        w206w=('%'+ str(search_data) +'%')
        ur_kod_1=session.query(directory_of_model).filter(directory_of_model.kod_model.ilike(w206w)).all()
        data_var=[]
        for row in ur_kod_1:
            data_var.append(row.kod_model)
        data_new_page = {"kod_model" : data_var}
#############################################################################    
    elif 'sl_phone' in data_from_new_page:
        search_data=data_from_new_page['sl_phone']
        data_new_page=return_data_from_client(search_data, 0)
####
    elif 'sl_second_name' in data_from_new_page:
        search_data=data_from_new_page['sl_second_name']
        data_new_page=return_data_from_client(0, search_data)
####
    elif 'sl_kod' in data_from_new_page:
        search_data=data_from_new_page['sl_kod']
        data_new_page=return_data_from_kod(search_data)
#############################################################################    
    elif 'sl_id_recipient' in data_from_new_page:
        data_tmp_page=return_data_from_full_person(data_from_new_page)
        if 'id_client' in data_tmp_page:
            w1w=data_tmp_page['id_client']
            data_new_page={"id_recipient" : w1w}
        else:
            data_new_page=data_tmp_page
####    
    elif 'sl_id_client' in data_from_new_page:
        data_new_page=return_data_from_full_person(data_from_new_page)
####
    elif 'sl_id_model' in data_from_new_page:
        # search_data=data_from_new_page['sl_kod']
        data_new_page=return_data_from_full_kod(data_from_new_page)

#############################################################################    
    else:
        data_new_page = {"this POST from WEB-page" : "not correctly"}
    # return data_new_page
    return json.dumps(data_new_page, ensure_ascii=False)