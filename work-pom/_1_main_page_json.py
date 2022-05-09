from distutils.command.clean import clean
import json
from flask import session 
from sqlalchemy import MetaData, false, func, true, text, Integer, String, Table, Column, insert, create_engine, \
    and_, or_, update
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session, mapper, declarative_base#, decl_base, decl_api#, desc
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine




def return_data_from_main_page(asked):
    with Session(engine) as session:
        id_order,comment_order,data_order,kolor_model,kod_model,comment_model,quantity_pars_model,\
            phase_1_model,phase_2_model,phase_3_model,sum_payment,real_money, \
            phone_client,sity,data_plane_order,fulfilled_order,np_number,zip_code, \
            street_house_apartment=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        one_blok,full_block=[],[]

        ds=datetime.today().strftime('%Y-%m-%d')
        if 'data_start' in asked: data_start=asked['data_start']
        else: data_start="2016-01-01"
        if 'data_end' in asked: data_end=asked['data_end']
        else: data_end=ds
        
        
        if 'fulfilled_order' in asked:
            fulfilled_order_1=asked['fulfilled_order']
        else: fulfilled_order_1=false
        if 'phone_client' in asked: 
            phone_client_tmp=str(asked['phone_client'])
            id_client_1=session.query(directory_of_client).filter_by(phone_client=phone_client_tmp).all()
            for row in id_client_1:
                # id_client=row.id_client
                id_order_1=session.query(directory_of_order).filter(directory_of_order.data_order>=data_start,
                directory_of_order.data_order<=data_end).filter_by(id_client=row.id_client).all()
        elif 'fulfilled_order' in asked:
            id_order_1=session.query(directory_of_order).filter(directory_of_order.data_order>=data_start,
            directory_of_order.data_order<=data_end).filter_by(fulfilled_order=fulfilled_order_1).all()
        else:
            id_order_1=session.query(directory_of_order).filter(directory_of_order.data_order>=data_start,
            directory_of_order.data_order<=data_end).all()
        for row in id_order_1:
            id_order.append(row.id_order)
            comment_order.append(row.comment_order)
            data_order.append(row.data_order)
            sum_payment.append(row.sum_payment)
            data_plane_order.append(row.data_plane_order)
            fulfilled_order.append(row.fulfilled_order)
        

        # print(id_order)



        full_block={"testdata" : "in progres", "data_end": data_end, "id_order":id_order}
    return json.dumps(full_block)