import json
from sqlalchemy import func
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import directory_of_order as db_o
from db.models import directory_of_client as db_c
from db.models import directory_of_payment as db_p
from db.models import directory_of_model as db_m
from db.models import engine


def get_main(get_query):
    try:
        with Session(engine) as session:
            df = datetime.today().strftime('%Y-%m-%d')
            ds = '2016-01-01'
            fulfilled = str('False')
            if 'data_start' in get_query:
                ds = get_query['data_start']
            if 'data_finish' in get_query:
                df = get_query['data_finish']
#
            id_client_list, id_model_list = [], []
            if 'phone_client' in get_query:
                phone_client = get_query['phone_client']
                pre_list = session.query(db_c).filter_by(
                    phone_client=phone_client).order_by(
                    'id_client').all()
                id_client_list = list_search(pre_list)
            elif 'second_name_client' in get_query:
                second_name_client = get_query['second_name_client']
                pre_list = session.query(db_c).filter_by(
                    second_name_client=second_name_client).order_by(
                    'id_client').all()
                id_client_list = list_search(pre_list)
            elif 'team' in get_query:
                team = get_query['team']
                pre_list = session.query(db_c).filter_by(
                    team=team).order_by(
                    'id_client').all()
                id_client_list = list_search(pre_list)
            elif 'coach' in get_query:
                coach = get_query['coach']
                pre_list = session.query(db_c).filter_by(
                    coach=coach).order_by(
                    'id_client').all()
                id_client_list = list_search(pre_list)
            elif 'sity' in get_query:
                sity = get_query['sity']
                pre_list = session.query(db_c).filter_by(
                    sity=sity).order_by(
                    'id_client').all()
                id_client_list = list_search(pre_list)
            elif 'kod_model' in get_query:
                id_model_list = []
                kod_model = get_query['kod_model']
                pre_list = session.query(db_m).filter_by(
                    kod_model=kod_model).order_by(
                    'id_model').all()
                for row in pre_list:
                    id_model_list.append(row.id_model)
#
            if 'fulfilled' in get_query:
                fulfilled = get_query['fulfilled']
            if fulfilled == 'all':
                if len(id_client_list) != 0:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df,
                        db_o.id_client.in_(id_client_list)).order_by(
                        'id_order').all()
                elif len(id_model_list) != 0:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df, sa.or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list))).order_by(
                        'id_order').all()
                else:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df).order_by(
                        'id_order').all()
            else:
                if len(id_client_list) != 0:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df, sa.or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list))).filter_by(
                        fulfilled_order=fulfilled).order_by(
                        'id_order').all()
                elif len(id_model_list) != 0:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df,
                        db_o.id_model.in_(id_model_list)).filter_by(
                        fulfilled_order=fulfilled).order_by(
                        'id_order').all()
                else:
                    list_order = session.query(db_o).filter(
                        db_o.data_order >= ds,
                        db_o.data_order <= df).filter_by(
                        fulfilled_order=fulfilled).order_by(
                        'data_plane_order').all()
#
            count_order = []
            for row in list_order:
                count_order.append(row.id_order)
            if len(count_order) == 0:
                id_order_max = session.query(func.max(
                    db_o.id_order)).first()
                tmp_order = int(id_order_max[0])
                list_order = session.query(db_o).filter_by(
                    id_order=tmp_order).all()
#
            full_block = []
            for row in list_order:
                m_id_order = row.id_order
                m_comment_order = row.comment_order
                m_data_order = (str(row.data_order))
                m_data_plane_order = (str(row.data_plane_order))
                m_fulfilled_order = (row.fulfilled_order)
                m_sum_payment = (row.sum_payment - row.discont_order)
                m_quantity_pars_model = (row.quantity_pars_model)
                m_phase_1 = row.phase_1
                m_phase_2 = row.phase_2
                m_phase_3 = row.phase_3
                m_id_model = row.id_model

                tmp_len_1 = len(m_id_model)
                m_kolor_model, m_kod_model, m_comment_model, = [], [], []
                while tmp_len_1 > 0:
                    tmp_len_1 -= 1
                    id_model = m_id_model.pop(0)
                    gr_model = session.query(db_m).filter_by(
                        id_model=id_model).all()
                    for row5 in gr_model:
                        m_kolor_model.append(row5.kolor_model)
                        m_kod_model.append(row5.kod_model)
                        m_comment_model.append(row5.comment_model)

                if len(list(m_quantity_pars_model)) == 1:
                    m_quantity_pars_model = m_quantity_pars_model[0]
                    m_phase_1 = m_phase_1[0]
                    m_phase_2 = m_phase_2[0]
                    m_phase_3 = m_phase_3[0]
                    m_kolor_model = m_kolor_model[0]
                    m_kod_model = m_kod_model[0]
                    m_comment_model = m_comment_model[0]
#
                id_client_2 = session.query(db_c).filter_by(
                    id_client=row.id_client).all()
                if (len(str(id_client_2))) < 3:
                    return json.dumps({
                        "Помилка в записі клієнта - id:": row.id_order}), 500
                for row1 in id_client_2:
                    m_phone_client = (row1.phone_client)
#
                id_recipient_1 = session.query(db_c).filter_by(
                    id_client=row.id_recipient).all()
                if (len(str(id_recipient_1))) < 3:
                    return json.dumps({
                     "Помилка в записі отримувача - id:": row.id_order}), 500
                for row1 in id_recipient_1:
                    m_second_name_client = (row1.second_name_client)
                    m_first_name_client = (row1.first_name_client)
                    m_phone_recipient = (row1.phone_client)
                    m_np_number = (row1.np_number)
                    m_zip_code = (row1.zip_code)
                    m_street_house_apartment = (row1.street_house_apartment)
                    m_sity = (row1.sity)
#
                real_money_1 = session.query(func.sum(
                    db_p.payment).label('my_sum')).filter_by(
                    id_order=row.id_order).first()
                m_real_money = (real_money_1.my_sum)

                one_block = {"id_order": m_id_order,
                             "comment_order": m_comment_order,
                             "data_order": m_data_order,
                             "kolor_model": m_kolor_model,
                             "kod_model": m_kod_model,
                             "comment_model": m_comment_model,
                             "quantity_pars_model": m_quantity_pars_model,
                             "phase_1": m_phase_1,
                             "phase_2": m_phase_2,
                             "phase_3": m_phase_3,
                             "sum_payment": m_sum_payment,
                             "real_money": m_real_money,
                             "phone_client": m_phone_client,
                             "phone_recipient": m_phone_recipient,
                             "sity": m_sity,
                             "data_plane_order": m_data_plane_order,
                             "fulfilled_order": m_fulfilled_order,
                             "np_number": m_np_number,
                             "zip_code": m_zip_code,
                             "street_house_apartment": m_street_house_apartment,  # noqa: E501
                             "second_name_client": m_second_name_client,
                             "first_name_client": m_first_name_client}
                full_block.append(one_block)
        return json.dumps(full_block)
#
    except Exception as e:
        return json.dumps(f'Error in function main: {e}')


def list_search(list_sql_in):
    list_sql_out = []
    for row in list_sql_in:
        list_sql_out.append(row.id_client)
    return list_sql_out
