import json 
from sqlalchemy import MetaData, false, func, true, text, Integer, String, Table, Column, insert, create_engine, \
    and_, or_, update#, desc
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session, mapper, declarative_base#, decl_base, decl_api#, desc
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine

def return_data_from_finance(asked):
    with Session(engine) as session:
        data_outlay_class=[]
        id_payment=[]
        id_order=[]
        payment=[]
        metod_payment=[]
        data_payment=[]
        full_block=[]
        id_outlay=[]
        data_outlay=[]
        id_outlay_class=[]
        money_outlay=[]
        comment_outlay=[]
        data_outlay_class_1=session.query(directory_of_outlay_class).all()
        for row in data_outlay_class_1:
            data_outlay_class.append(row.outlay_class)
        data_last_payment_1=session.query(directory_of_payment).order_by(directory_of_payment.id_payment.desc()).limit(3)
        for row in data_last_payment_1:
            id_payment.append(row.id_payment)
            id_order.append(row.id_order)
            payment.append(row.payment)
            metod_payment.append(row.metod_payment)
            data_payment.append(str(row.data_payment))
        data_last_outlay_1=session.query(directory_of_outlay).order_by(directory_of_outlay.id_outlay.desc()).limit(1)
        for row in data_last_outlay_1:
            id_outlay.append(row.id_outlay)
            data_outlay.append(str(row.data_outlay))
            id_outlay_class.append(row.id_outlay_class)
            money_outlay.append(row.money_outlay)
            comment_outlay.append(row.comment_outlay)

        one_block={"metod_payment" : ["iban", "cash"], "outlay_class": data_outlay_class}
        full_block.append(one_block)
        q1=block_json(id_payment, id_order, payment, metod_payment, data_payment)
        q11={"id_payment":q1[0],"id_order":q1[1],"payment":q1[2],"metod_payment":q1[3],"data_payment":q1[4]}
        q1=block_json(id_payment, id_order, payment, metod_payment, data_payment)
        q12={"id_payment":q1[0],"id_order":q1[1],"payment":q1[2],"metod_payment":q1[3],"data_payment":q1[4]}
        q1=block_json(id_payment, id_order, payment, metod_payment, data_payment)
        q13={"id_payment":q1[0],"id_order":q1[1],"payment":q1[2],"metod_payment":q1[3],"data_payment":q1[4]}
        full_block.append(q13)
        full_block.append(q12)
        full_block.append(q11)

        q4=block_json(id_outlay,data_outlay,id_outlay_class,money_outlay,comment_outlay)
        one_block={"id_outlay":q4[0],"data_outlay":q4[1],"id_outlay_class":q4[2],"money_outlay":q4[3],"comment_outlay":q4[4]}
        full_block.append(one_block)
    return json.dumps(full_block)

def return_data_from_payment(sender):
    with Session(engine) as session:
        w1=sender[0]['payment_group']
        while w1>0:
            w1-=1
            w2=sender[1]
            del sender[1]
            z1=directory_of_payment(id_order=w2['id_order'],payment=w2['payment'],metod_payment=w2['metod_payment'],
                data_payment=w2['data_payment'])
            session.add(z1)
        session.commit()    
    return({"payment_group":"ok"})

def return_data_from_outlay(sender):
    with Session(engine) as session:
        w1=sender[0]['outlay_group']
        while w1>0:
            w1-=1
            w2=sender[1]
            del sender[1]
            z1=directory_of_outlay(data_outlay=w2['data_outlay'],id_outlay_class=w2['id_outlay_class'],money_outlay=w2['money_outlay'],
                comment_outlay=w2['comment_outlay'])
            session.add(z1)
        session.commit()    
    return({"outlay_group":"ok"})


def block_json(pos1,pos2,pos3,pos4,pos5):
    el1=pos1[0]
    del pos1[0]
    el2=pos2[0]
    del pos2[0]
    el3=pos3[0]
    del pos3[0]
    el4=pos4[0]
    del pos4[0]
    el5=pos5[0]
    del pos5[0]
    return [el1,el2,el3,el4,el5]

