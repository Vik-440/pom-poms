# from time import time
from operator import and_, or_
from unicodedata import numeric
from sqlalchemy import create_engine,  MetaData, true, text, Integer, String, Table, Column, and_, or_
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model, \
        directory_of_group, directory_of_payment, directory_of_sity, directory_of_color, \
        directory_of_outlay, directory_of_outlay_class
#Base = declarative_base()
from data_pompom_create import engine

def return_data_from_sql(data_start_order, data_end_order):
    # time_start=datetime.today().strftime('%Y-%m-%d : %H-%M-%S----%f')

    Session = sessionmaker(engine)
    Session.configure(bind=engine)
    session = Session()
    j_id_order=[]
    j_data_order=[]
    j_data_plane_order=[]
    j_sum_payment=[]
    j_kolor_model = []
    j_kolor_model_1 = []
    j_kod_model = []
    j_kod_model_1 = []
    j_quantity_pars_model=[]
    j_phase_1_model=[]
    j_phase_2_model=[]
    j_phase_3_model=[]
    j_id_recipient=[]
    j_id_sity=[]
    j_sity=[]
    j_real_money=[]
    j_comment_model=[]
    j_comment_order=[]
    j_fulfilled_order=[]
    comment_order_2=[]
    # w21w=[]
    
    if data_start_order !=0 and data_end_order !=0:
        # if data_end_order !=0:
        id_order_1=session.query(directory_of_order).filter(directory_of_order.data_order>=data_start_order,
        directory_of_order.data_order<=data_end_order).all()
    else:
        id_order_1=session.query(directory_of_order).filter_by(fulfilled_order='FALSE').order_by('id_order').all()

    for row in id_order_1:      # робочий 2 яруси отримання данних
        j_id_order.append(row.id_order)
        #
        quantity_pars_model_1=session.query(directory_of_group).filter_by(id_order=row.id_order).order_by('quantity_pars_model').all()
        w1w=len(quantity_pars_model_1)
        w2w=[]   ### тут змінювати тип данних
        for row1 in quantity_pars_model_1:
            if w1w > 0:
                w2w.append(row1.quantity_pars_model)   ### тут змінювати метод додавання
                w1w=w1w-1
        if len(w2w)== 1:
            w2w=w2w[0]
        j_quantity_pars_model.append(w2w)



#############################################################################################################
        phase_1_model_1=session.query(directory_of_group).filter_by(id_order=row.id_order).order_by('phase_1_model').all()
        # for row1 in phase_1_model_1:
        #     j_phase_1_model.append(row1.phase_1_model)
        w1w=len(phase_1_model_1)
        # print(w1w)
        w2w=[]   ### тут змінювати тип данних
        for row1 in phase_1_model_1:
            if w1w > 0:
                w2w.append(row1.phase_1_model)   ### тут змінювати метод додавання
                w1w=w1w-1
        if len(w2w)== 1:
            w2w=w2w[0]
        j_phase_1_model.append(w2w)

############################################################################################################        
        phase_2_model_1=session.query(directory_of_group).filter_by(id_order=row.id_order).order_by('phase_2_model').all()
        # for row1 in phase_2_model_1:
        #     j_phase_2_model.append(row1.phase_2_model)
        w1w=len(phase_2_model_1)
        # print(w1w)
        w2w=[]   ### тут змінювати тип данних
        for row1 in phase_2_model_1:
            if w1w > 0:
                w2w.append(row1.phase_2_model)   ### тут змінювати метод додавання
                w1w=w1w-1
        if len(w2w)== 1:
            w2w=w2w[0]
        j_phase_2_model.append(w2w)

        phase_3_model_1=session.query(directory_of_group).filter_by(id_order=row.id_order).order_by('phase_3_model').all()
        # for row1 in phase_3_model_1:
        #     j_phase_3_model.append(row1.phase_3_model)
        w1w=len(phase_3_model_1)
        # print(w1w)
        w2w=[]   ### тут змінювати тип данних
        for row1 in phase_3_model_1:
            if w1w > 0:
                w2w.append(row1.phase_3_model)   ### тут змінювати метод додавання
                w1w=w1w-1
        if len(w2w)== 1:
            w2w=w2w[0]
        j_phase_3_model.append(w2w)

################################################################################################################
        id_model_1=session.query(directory_of_group).filter_by(id_order=row.id_order).order_by('id_model').all()
        w1w=len(id_model_1)
        w10w=len(id_model_1)
        w100w=len(id_model_1)
        w202w=[]
        w20w=[] 
        w201w=[]
        for row1 in id_model_1:
            zzz=row1.id_model
####   kolor_model        
            kolor_model_1=session.query(directory_of_model).filter_by(id_model=row1.id_model).all()
            for row6 in kolor_model_1:               #### тут шукати помилку!
                w222w=row6.kolor_model
                if w1w > 0:
                    w202w.append(w222w)   ### тут змінювати метод додавання
                    w1w=w1w-1
####   kod_model             
            kod_model_1=session.query(directory_of_model).filter_by(id_model=zzz).all()
            for row5 in kod_model_1:                #### тут шукати помилку!
                w223w=row5.kod_model
                if w10w > 0:
                    w20w.append(w223w)   ### тут змінювати метод додавання
                    w10w=w10w-1
####   comment_model 
            comment_model_1=session.query(directory_of_model).filter_by(id_model=zzz).all()
            for row2 in comment_model_1:
                w224w=row2.comment_model
                if w100w > 0:
                    w201w.append(w224w)
                    w100w=w100w-1
####
        if len(w202w)== 1:
            w202w=w202w[0]
        j_kolor_model.append(w202w)
        if len(w20w)== 1:
                w20w=w20w[0]
        j_kod_model.append(w20w)
        if len(w201w)== 1:
                w201w=w201w[0]
        j_comment_model.append(w201w)
####       
        # j_kod_model_1=j_kod_model
        # j_kolor_model_1=['бірюзовий', 'червоний', ['синій', 'бірюзовий', 'білий + синій'],
            # 'Срібна (гол) + Рожевий', 'Малиновий']

###############################################################################################################
        id_recipient_1=session.query(directory_of_order).filter_by(id_order=row.id_order).order_by('id_recipient').all() 
        for row3 in id_recipient_1:
            id_sity_1=session.query(directory_of_client).filter_by(id_client=row3.id_recipient).order_by('id_sity').all()
            for row4 in id_sity_1:
                sity_1=session.query(directory_of_sity).filter_by(id_sity=row4.id_sity).order_by('sity').all()
                for row5 in sity_1:
                    j_sity.append(row5.sity)
        
        sum_payment_1=session.query(directory_of_order).filter_by(id_order=row.id_order).all() 
        for row3 in sum_payment_1:
            x1x=row3.sum_payment
            x2x=row3.discont_order
            x3x=x1x - x2x
            j_sum_payment.append(int(x3x))
#####################################################################################################3            
        real_money_1=session.query(directory_of_payment).filter_by(id_order=row.id_order).all()
        q3q=(len(real_money_1))
        if q3q == 0:
            j_real_money.append(0)
        else:
            q2q=0
            for row5 in real_money_1:
                q4q=row5.payment
                if q3q > 0:
                    q2q=q2q+q4q
                    q3q=q3q-1
            j_real_money.append(int(q2q))

        data_plane_order_1=session.query(directory_of_order).filter_by(id_order=row.id_order).all()
        for row3 in data_plane_order_1:
            j_data_plane_order.append(str(row3.data_plane_order))
        
        data_order_1=session.query(directory_of_order).filter_by(id_order=row.id_order).all()
        for row3 in data_order_1:
            j_data_order.append(str(row3.data_order))

        comment_order_1=session.query(directory_of_order).filter_by(id_order=row.id_order).all()
        for row3 in comment_order_1:
            w205w=[]
            w205w = row3.comment_order
            j_comment_order.append(w205w)
            # j_comment_order.append(str(row3.comment_order))

        fulfilled_order_1=session.query(directory_of_order).filter_by(id_order=row.id_order).all()
        for row3 in fulfilled_order_1:
            j_fulfilled_order.append(row3.fulfilled_order)

    # time_stop=datetime.today().strftime('%Y-%m-%d : %H-%M-%S----%f')

        
    return {'id_order': j_id_order,
            'data_order': j_data_order,
            'kolor_model': j_kolor_model,
            'kolor_model_1': j_kolor_model_1,
            'kod_model': j_kod_model,
            'kod_model_1': j_kod_model_1,
            'quantity_pars_model': j_quantity_pars_model,
            'phase_1_model': j_phase_1_model,
            'phase_2_model': j_phase_2_model,
            'phase_3_model': j_phase_3_model,
            'sity': j_sity,
            'sum_payment': j_sum_payment,
            'real_money': j_real_money,
            'data_plane_order': j_data_plane_order,
            'comment_order': j_comment_order,
            'comment_model': j_comment_model,
            'fulfilled_order' : j_fulfilled_order
        }


# print('id_order - ', j_id_order)
# print('data_order - ', j_data_order)
# print('kolor_model - ', j_kolor_model)
# print('kolor_model_1 - ', j_kolor_model_1)
# print('kod_model - ', j_kod_model)
# print('kod_model_1 - ', j_kod_model_1)
# print('quantity_pars_model - ', j_quantity_pars_model)
# print('phase_1_model - ', j_phase_1_model)
# print('phase_2_model - ', j_phase_2_model)
# print('phase_3_model - ', j_phase_3_model)
# print('sity - ', j_sity)
# print('sum_payment - ', j_sum_payment)
# print('real_money - ', j_real_money)
# print('data_plane_order - ', j_data_plane_order)
# print('comment_order - ', j_comment_order)
# print('comment_model - ', j_comment_model)


# print ('час запуску - ', datetime.today().strftime('%Y-%m-%d : %H-%M-%S----%f'))
# print('початок програми - ', time_start)
# print('кінець програми  - ', time_stop)