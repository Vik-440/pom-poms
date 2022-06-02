from operator import and_, or_
from unicodedata import numeric
# from pymysql import NULL
from sqlalchemy import create_engine,  MetaData, false, func, null, true, text, Integer, String, Table, Column, insert
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine


###################################################################################
def return_data_from_order_page():
    with Session(engine) as session:
        id_new_order=session.query(func.max(directory_of_order.id_order))
        for row222 in id_new_order:
            j_id_new_order=row222[0]+1
        time_last_order = '2022-12-31'
        # session.close()
        return {'id_new_order':j_id_new_order, 'time_last_order':time_last_order}
################################################################################### - тут дописати пошук по ID
def return_data_from_client(sl_phone, sl_second_name, open_id_client):
    with Session(engine) as session:

        if sl_phone==0 and open_id_client==0:
            id_client_3=session.query(directory_of_client).filter_by(second_name_client=sl_second_name).all()
        elif sl_second_name==0 and open_id_client==0:
            sl_phone=str(sl_phone)
            id_client_3=session.query(directory_of_client).filter_by(phone_client=str(sl_phone)).all() 
        else:
            id_client_3=session.query(directory_of_client).filter_by(id_client=open_id_client).all()
########
        for row in id_client_3:
            j_id_client=row.id_client
            id_sity=row.id_sity
            id_team=row.id_team
        phone_client_1=session.query(directory_of_client).filter_by(id_client=j_id_client).all()

        for row1 in phone_client_1:
            j_phone_client=(row1.phone_client)
            j_second_name_client=(row1.second_name_client)
            j_first_name_client=(row1.first_name_client)
            j_surname_client=(row1.surname_client)
            j_np_number=(row1.np_number)
            j_coach=(row1.coach)
            j_zip_code=(row1.zip_code)
            j_street_house_apartment=(row1.street_house_apartment)
            j_comment_client=(row1.comment_client)

            sity_1=session.query(directory_of_sity).filter_by(id_sity=id_sity).all()
            for row2 in sity_1:
                j_sity=(row2.sity)
            name_team_1=session.query(directory_of_team).filter_by(id_team=id_team).all()
            for row2 in name_team_1:
                j_name_team=(row2.name_team)


        one_block = {"id_client": j_id_client, "phone_client": j_phone_client, "second_name_client" : j_second_name_client,
        "first_name_client" : j_first_name_client, "surname_client" : j_surname_client, "sity" : j_sity,
        "np_number" : j_np_number, "name_team" : j_name_team, "coach":j_coach, "zip_code": j_zip_code,
        "street_house_apartment": j_street_house_apartment, "comment_client": j_comment_client}

    return one_block

###################################################################################
def return_data_from_kod(sl_kod,open_id_model):
    with Session(engine) as session:
        if open_id_model==0:
            id_model_1=session.query(directory_of_model).filter_by(kod_model=sl_kod).all()
        else:
            id_model_1=session.query(directory_of_model).filter_by(id_model=open_id_model).all()
        for row in id_model_1:
            j_id_model=row.id_model
            j_kod_model=row.kod_model
            j_id_color_1=row.id_color_1
            j_id_color_part_1=row.id_color_part_1
            j_id_color_2=row.id_color_2
            j_id_color_part_2=row.id_color_part_2
            j_id_color_3=row.id_color_3
            j_id_color_part_3=row.id_color_part_3
            j_id_color_4=row.id_color_4
            j_id_color_part_4=row.id_color_part_4
            j_price_model=row.price_model
            j_comment_model=row.comment_model
            j_kolor_model=row.kolor_model
        
        name_color_0=session.query(directory_of_color).filter_by(id_color=j_id_color_1).all()
        for row in name_color_0:
            name_color_1=row.name_color
        if j_id_color_2!=0 and j_id_color_2!=None:
            name_color_0=session.query(directory_of_color).filter_by(id_color=j_id_color_2).all()
            for row in name_color_0:
                name_color_2=row.name_color
        else: name_color_2=0
        if j_id_color_3!=0 and j_id_color_3!=None:
            name_color_0=session.query(directory_of_color).filter_by(id_color=j_id_color_3).all()
            for row in name_color_0:
                name_color_3=row.name_color
        else: name_color_3=0
        if j_id_color_4!=0 and j_id_color_4!=None :  # 
            name_color_0=session.query(directory_of_color).filter_by(id_color=j_id_color_4).all()
            for row in name_color_0:
                name_color_4=row.name_color
        else: name_color_4=0
        
        if len(str(id_model_1))<3:
            one_block={}
        else:
            one_block = {"id_model":j_id_model, "kod_model":j_kod_model, "id_color_1":j_id_color_1,
            "name_color_1":name_color_1,"id_color_part_1":j_id_color_part_1, "id_color_2":j_id_color_2,
            "name_color_2":name_color_2,"id_color_part_2":j_id_color_part_2,"id_color_3":j_id_color_3,
            "name_color_3":name_color_3,"id_color_part_3":j_id_color_part_3, "id_color_4":j_id_color_4,
            "name_color_4":name_color_4,"id_color_part_4":j_id_color_part_4, "price_model":j_price_model,
            "comment_model":j_comment_model,"kolor_model":j_kolor_model}
    return one_block
###################################################################################
def return_data_from_full_kod(data_from_new_page):
    with Session(engine) as session:
        j_id_model=0
        search_data=data_from_new_page['kod_model']
        id_model_1=session.query(directory_of_model).filter_by(kod_model=search_data).all()
        for row in id_model_1:
            j_id_model=row.id_model
        if j_id_model ==0:
            ins = directory_of_model(
                    kod_model=data_from_new_page['kod_model'],
                    id_color_1=data_from_new_page['id_color_1'],
                    id_color_part_1=data_from_new_page['id_color_part_1'],
                    id_color_2=data_from_new_page['id_color_2'],
                    id_color_part_2=data_from_new_page['id_color_part_2'],
                    id_color_3=data_from_new_page['id_color_3'],
                    id_color_part_3=data_from_new_page['id_color_part_3'],
                    id_color_4=data_from_new_page['id_color_4'],
                    id_color_part_4=data_from_new_page['id_color_part_4'],
                    price_model=data_from_new_page['price_model'],
                    comment_model=data_from_new_page['comment_model'],
                    kolor_model=data_from_new_page['kolor_model'])
            session.add(ins)
            session.commit()

            id_model_1=session.query(directory_of_model).filter_by(kod_model=search_data).all()
            for row in id_model_1:
                j_id_model=row.id_model
            one_block = {"id_model" : j_id_model}
        else:
            q1q=('real_id=' + str(j_id_model))
            one_block = {"id_model" : q1q}
        return one_block
###################################################################################
def return_data_from_full_person(data_from_new_page):
    with Session(engine) as session:
        j_second_name_client=0
        search_data=str(data_from_new_page['phone_client'])
        second_name_client_1=session.query(directory_of_client).filter_by(phone_client=search_data).all()
        for row in second_name_client_1:
            j_second_name_client=row.second_name_client
        if j_second_name_client ==0:
            ins = directory_of_client(
                    phone_client=data_from_new_page['phone_client'],
                    second_name_client=data_from_new_page['second_name_client'],
                    first_name_client=data_from_new_page['first_name_client'],
                    surname_client=data_from_new_page['surname_client'],
                    id_sity=data_from_new_page['id_sity'],
                    np_number=data_from_new_page['np_number'],
                    id_team=data_from_new_page['id_team'],
                    coach=data_from_new_page['coach'],
                    zip_code=data_from_new_page['zip_code'],
                    street_house_apartment=data_from_new_page['street_house_apartment'],
                    comment_client=data_from_new_page['comment_client'])
    
            session.add(ins)
            session.commit()

            id_client_1=session.query(directory_of_client).filter_by(phone_client=search_data).all()
            for row in id_client_1:
                j_id_client=row.id_client
            one_block = {"id_client" : j_id_client}
        else:
            q1q=('даний номер телефону уже існує в базі з прізвищем - ' + str(j_second_name_client))
            one_block = {"phone_client" : q1q}
        return one_block
###################################################################################
def return_data_from_final_order(data_from_new_page):
    with Session(engine) as session:
        id_order=data_from_new_page['id_order']
        if id_order ==0:
            ins=directory_of_order(
                data_order=data_from_new_page['data_order'],
                id_client=data_from_new_page['id_client'],
                id_recipient=data_from_new_page['id_recipient'],
                data_plane_order=data_from_new_page['data_plane_order'],
                data_send_order=data_from_new_page['data_send_order'],
                discont_order=data_from_new_page['discont_order'],
                sum_payment=data_from_new_page['sum_payment'],
                fulfilled_order=data_from_new_page['fulfilled_order'],
                comment_order=data_from_new_page['comment_order'])
        else:
            ins=directory_of_order(
                id_order=id_order,
                data_order=data_from_new_page['data_order'],
                id_client=data_from_new_page['id_client'],
                id_recipient=data_from_new_page['id_recipient'],
                data_plane_order=data_from_new_page['data_plane_order'],
                data_send_order=data_from_new_page['data_send_order'],
                discont_order=data_from_new_page['discont_order'],
                sum_payment=data_from_new_page['sum_payment'],
                fulfilled_order=data_from_new_page['fulfilled_order'],
                comment_order=data_from_new_page['comment_order'])
        session.add(ins)
        session.commit()
        session.refresh(ins)
        j_id_order=ins.id_order

        w1w=len(data_from_new_page['id_model'])
        # print(w1w)
        while w1w>0:
            elem1=data_from_new_page['id_model'][0]
            del data_from_new_page['id_model'][0]
            elem2=data_from_new_page['quantity_pars_model'][0]
            del data_from_new_page['quantity_pars_model'][0]

            ins1=directory_of_group(
                id_order=j_id_order,
                phase_1_model=False,
                phase_2_model=False,
                phase_3_model=False,
                id_model=elem1,
                quantity_pars_model=elem2)
            session.add(ins1)
            session.commit()
            w1w=w1w-1
        
        one_block = {"id_order" : j_id_order}
        return one_block
###################################################################################
def return_data_from_edit_order(data_from_new_page):
    with Session(engine) as session:
        edit_order=data_from_new_page['edit_order']
        id_order_1=session.query(directory_of_order).filter_by(id_order=edit_order).all()
        for row in id_order_1:
            id_order=row.id_order
            data_order=str(row.data_order)
            id_client=row.id_client
            id_recipient=row.id_recipient
            data_plane_order=str(row.data_plane_order)
            data_send_order=str(row.data_send_order)
            discont_order=row.discont_order
            sum_payment=row.sum_payment
            fulfilled_order=row.fulfilled_order
            comment_order=row.comment_order
            
            id_model,quantity_pars_model=[],[]
            id_model_1=session.query(directory_of_group).filter_by(id_order=id_order)
            for row1 in id_model_1:
                id_model.append(row1.id_model)
                quantity_pars_model.append(row1.quantity_pars_model)

        if len(str(id_order_1))<3:
            one_block={}
        else:
            one_block = {"id_order":id_order,"data_order":data_order,"id_client":id_client,"id_recipient":id_recipient,
            "data_plane_order":data_plane_order,"data_send_order":data_send_order,"discont_order":discont_order,
            "sum_payment":sum_payment,"fulfilled_order":fulfilled_order,"comment_order":comment_order,
            "id_model":id_model,"quantity_pars_model":quantity_pars_model}

    return one_block