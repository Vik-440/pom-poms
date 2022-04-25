from operator import and_, or_
from unicodedata import numeric
from sqlalchemy import create_engine,  MetaData, false, func, true, text, Integer, String, Table, Column, insert
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class


log_pass_sql = 'postgresql+psycopg2://postgres:123123@localhost/postgres'
engine = create_engine(log_pass_sql)

# Session = sessionmaker(engine)
# Session.configure(bind=engine)
# session = Session()

# j_id_client=[]
# j_phone_client=[]
###################################################################################
def return_data_from_order_page():
    with Session(engine) as session:
        id_new_order=session.query(func.max(directory_of_order.id_order))
        for row222 in id_new_order:
            j_id_new_order=row222[0]+1
        time_last_order = '2022-22-22'
        # session.close()
        return {'id_new_order':j_id_new_order, 'time_last_order':time_last_order}
###################################################################################
def return_data_from_client(sl_phone, sl_second_name):
    with Session(engine) as session:
        # j_phone_client.clear()
        j_phone_client=[]
        j_id_client=[]
        j_second_name_client=[]
        j_first_name_client=[]
        j_surname_client=[]
        j_sity=[]
        j_np_number=[]
        j_name_team=[]
        j_coach=[]
        j_zip_code=[]
        j_street_house_apartment=[]
        j_comment_client=[]

        if sl_phone==0:
            id_client_1=session.query(directory_of_client).filter_by(second_name_client=sl_second_name).all()
        else:
            sl_phone=str(sl_phone)
            # print(sl_phone)
            id_client_1=session.query(directory_of_client).filter_by(phone_client=str(sl_phone)).all()    
######## тут        
        for row in id_client_1:
            j_id_client.append(row.id_client)
    
            phone_client_1=session.query(directory_of_client).filter_by(id_client=row.id_client).all()
            w1w=len(phone_client_1)
            w2w=[]
            w3w=[]
            w4w=[]
            w5w=[]
            w6w=[]
            w7w=[]
            w8w=[]
            w9w=[]
            w10w=[]
            w11w=[]
            w12w=[]
            for row1 in phone_client_1:
                if w1w > 0:
                    w2w.append(row1.phone_client)
                    w3w.append(row1.second_name_client)
                    w4w.append(row1.first_name_client)
                    w5w.append(row1.surname_client)
                    w6w.append(row1.np_number)
                    w7w.append(row1.coach)
                    w8w.append(row1.zip_code)
                    w9w.append(row1.street_house_apartment)
                    w10w.append(row1.comment_client)
                    # w12w.append(row1.id_team)
                    sity_1=session.query(directory_of_sity).filter_by(id_sity=row.id_sity).all()
                    for row2 in sity_1:
                        w11w.append(row2.sity)
                    name_team_1=session.query(directory_of_team).filter_by(id_team=row.id_team).all()
                    for row2 in name_team_1:
                        w12w.append(row2.name_team)

                    w1w=w1w-1
            if len(w2w)== 1:
                w2w=int(w2w[0])
            j_phone_client.append(w2w)
            if len(w3w)== 1:
                w3w=w3w[0]
            j_second_name_client.append(w3w)
            if len(w4w)== 1:
                w4w=w4w[0]
            j_first_name_client.append(w4w)
            if len(w5w)== 1:
                w5w=w5w[0]
            j_surname_client.append(w5w)
            if len(w6w)== 1:
                w6w=int(w6w[0])
            j_np_number.append(w6w)
            if len(w7w)== 1:
                w7w=w7w[0]
            j_coach.append(w7w)
            if len(w8w)== 1:
                w8w=w8w[0]
            j_zip_code.append(w8w)
            if len(w9w)== 1:
                w9w=w9w[0]
            j_street_house_apartment.append(w9w)
            if len(w10w)== 1:
                w10w=w10w[0]
            j_comment_client.append(w10w)
            if len(w11w)== 1:
                w11w=w11w[0]
            j_sity.append(w11w)
            if len(w12w)== 1:
                w12w=w12w[0]
            j_name_team.append(w12w)

        a1a=len(j_id_client)
        full_block=[]
        # # print(a1a)
        while a1a > 0:
            a1a-=1
            element_1=j_id_client[0]
            del j_id_client[0]
            element_2=j_phone_client[0]
            del j_phone_client[0]
            element_3=j_second_name_client[0]
            del j_second_name_client[0]
            element_4=j_first_name_client[0]
            del j_first_name_client[0]
            element_5=j_surname_client[0]
            del j_surname_client[0]
            element_6=j_sity[0]
            del j_sity[0]
            element_7=j_np_number[0]
            del j_np_number[0]
            element_8=j_name_team[0]
            del j_name_team[0]
            element_9=j_coach[0]
            del j_coach[0]
            element_10=j_zip_code[0]
            del j_zip_code[0]
            element_11=j_street_house_apartment[0]
            del j_street_house_apartment[0]
            element_12=j_comment_client[0]
            del j_comment_client[0]

            one_block = {"id_client": element_1, "phone_client": element_2, "second_name_client" : element_3,
            "first_name_client" : element_4, "surname_client" : element_5, "sity" : element_6,
            "np_number" : element_7, "name_team" : element_8, "coach":element_9, "zip_code": element_10,
            "street_house_apartment": element_11, "comment_client": element_12}

            full_block.append(one_block)
    return full_block

###################################################################################
def return_data_from_kod(sl_kod):
    with Session(engine) as session:
        j_id_model=[]
        j_kod_model=[]
        j_id_color_1=[]
        j_id_color_part_1=[]
        j_id_color_2=[]
        j_id_color_part_2=[]
        j_id_color_3=[]
        j_id_color_part_3=[]
        j_id_color_4=[]
        j_id_color_part_4=[]
        j_price_model=[]
        j_comment_model=[]
        j_kolor_model=[]

        id_model_1=session.query(directory_of_model).filter_by(kod_model=sl_kod).all()
        for row in id_model_1:
            # a1a=len(row.id_model)
            # print(a1a)
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
        # print(len(str(j_kod_model)))
        if len(str(j_kod_model))<3:
            one_block={}
        else:
            one_block = {"id_model":j_id_model, "kod_model":j_kod_model, "id_color_1":j_id_color_1,
            "id_color_part_1":j_id_color_part_1, "id_color_2":j_id_color_2, "id_color_part_2":j_id_color_part_2,
            "id_color_3":j_id_color_3, "id_color_part_3":j_id_color_part_3, "id_color_4":j_id_color_4,
            "id_color_part_4":j_id_color_part_4, "price_model":j_price_model, "comment_model":j_comment_model,
            "kolor_model":j_kolor_model}

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
            q1q=('даний код моделі існує під номером : id=' + str(j_id_model))
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
        ins=directory_of_order(
            data_order=data_from_new_page['data_order'],
            id_client=data_from_new_page['id_client'],
            id_recipient=data_from_new_page['id_recipient'],
            data_plane_order=data_from_new_page['data_plane_order'],
            data_send_order=data_from_new_page['data_send_order'],
            discont_order=data_from_new_page['discont_order'],
            sum_payment=data_from_new_page['sum_payment'],
            fulfilled_order=data_from_new_page['fulfilled_order'])
        session.add(ins)
        session.commit()
        session.refresh(ins)
        j_id_order=ins.id_order

        w1w=len(data_from_new_page['id_model'])
        print(w1w)
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





#    "id_model" : [122, 21, 17, 114, 7],
#    "quantity_pars_model" : [2, 4, 2, 5, 15],

#return_data_from_final_order

# id_new_order=session.query(func.max(directory_of_order.id_order))
# for row in id_new_order:
#     j_id_new_order=row[0]
# time_last_order = '2022-04-24'
# print (j_id_new_order)