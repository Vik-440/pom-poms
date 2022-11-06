import json
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import directory_of_order, directory_of_client
from db.models import directory_of_payment
from db.models import directory_of_model
from db.models import engine


def change_main_phase(id_order, inform):
    with Session(engine) as session:
        check_sum = 0
        if 'phase_1' in inform:
            phase_int = inform['phase_1']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(directory_of_order).filter(
                    directory_of_order.id_order == id_order).update({
                        "phase_1": phase_int})
        elif 'phase_2' in inform:
            phase_int = inform['phase_2']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(directory_of_order).filter(
                    directory_of_order.id_order == id_order).update({
                        "phase_2": phase_int})
        elif 'phase_3' in inform:
            phase_int = inform['phase_3']
            for row in phase_int:
                check_sum = check_sum + row
            session.query(directory_of_order).filter(
                    directory_of_order.id_order == id_order).update({
                        "phase_3": phase_int})
        else:
            one_block = {"phase_chenged": "error"}
            return one_block

        session.commit()
        one_block = {"check_sum_phase": check_sum}
    return one_block


def return_data_from_main_page(asked):
    with Session(engine) as session:
        if 'fulfilled_id_order' in asked:
            id_order = asked['fulfilled_id_order']
            fulfilled_order = asked['fulfilled_order']
            if asked['fulfilled_order'] is False:
                session.query(directory_of_order).filter_by(
                    id_order=id_order).update(
                        {'fulfilled_order': fulfilled_order})
            else:
                res_ph = []
                ch_ph = session.query(directory_of_order.phase_1).filter_by(
                    id_order=id_order).all()
                for www in ch_ph:
                    for k in www.phase_1:
                        res_ph.append(0)
                ds = datetime.today().strftime('%Y-%m-%d')
                session.query(directory_of_order).filter_by(
                    id_order=id_order).update(
                        {'fulfilled_order': fulfilled_order,
                         'phase_1': res_ph, 'phase_2': res_ph,
                         'phase_3': res_ph,
                         'data_plane_order': ds})

            session.commit()
            one_block = {"id_order": "ok"}
            return json.dumps(one_block)

        id_order, full_block = [], []
        ds = datetime.today().strftime('%Y-%m-%d')
        if 'data_start' in asked:
            data_start = asked['data_start']
        else:
            data_start = "2016-01-01"
        if 'data_end' in asked:
            data_end = asked['data_end']
        else:
            data_end = ds

        id_client3 = []
        if 'fulfilled_order' in asked:
            fulfilled_order_1 = asked['fulfilled_order']
        if 'phone_client' in asked:
            phone_client_tmp = str(asked['phone_client'])
            id_client_1 = session.query(directory_of_client).filter_by(
                phone_client=phone_client_tmp).all()
            for row0 in id_client_1:
                id_client3 = row0.id_client
        if 'phone_client' in asked:
            if 'fulfilled_order' in asked:
                if fulfilled_order_1:
                    id_order_1 = session.query(directory_of_order).filter(
                        directory_of_order.data_order >= data_start,
                        directory_of_order.data_order <= data_end).filter_by(
                        fulfilled_order=fulfilled_order_1,
                        id_client=id_client3).order_by('id_order').all()
                else:
                    id_order_1 = session.query(directory_of_order).filter(
                        directory_of_order.data_order >= data_start,
                        directory_of_order.data_order <= data_end).filter_by(
                        id_client=id_client3).order_by('id_order').all()
            else:
                id_order_1 = session.query(directory_of_order).filter(
                    directory_of_order.data_order >= data_start,
                    directory_of_order.data_order <= data_end).filter_by(
                    fulfilled_order='FALSE', id_client=id_client3).order_by(
                    'id_order').all()
        elif 'fulfilled_order' in asked:
            if fulfilled_order_1:
                id_order_1 = session.query(directory_of_order).filter(
                    directory_of_order.data_order >= data_start,
                    directory_of_order.data_order <= data_end).filter_by(
                    fulfilled_order=fulfilled_order_1).order_by(
                    'id_order').all()
            else:
                id_order_1 = session.query(directory_of_order).filter(
                    directory_of_order.data_order >= data_start,
                    directory_of_order.data_order <= data_end).order_by(
                    'id_order').all()
# =
        else:
            id_order_1 = session.query(directory_of_order).filter(
                directory_of_order.data_order >= data_start,
                directory_of_order.data_order <= data_end).filter_by(
                fulfilled_order='FALSE').order_by('data_plane_order').all()
# =
        count_order = []
        for roww in id_order_1:
            count_order.append(roww.id_order)
        if len(count_order) == 0:
            id_order_max = session.query(func.max(
                directory_of_order.id_order)).first()
            tmp_order = int(id_order_max[0])
            id_order_1 = session.query(directory_of_order).filter_by(
                id_order=tmp_order).all()

        for row in id_order_1:
            m_id_order = row.id_order
            m_comment_order = row.comment_order
            m_data_order = (str(row.data_order))
            m_data_plane_order = (str(row.data_plane_order))
            m_fulfilled_order = (row.fulfilled_order)
            m_sum_payment = (row.sum_payment - row.discont_order)
            m_quantity_pars_model = (row.quantity_pars_model)
            # m_phase_1_model = row.phase_1_model
            # m_phase_2_model = row.phase_2_model
            # m_phase_3_model = row.phase_3_model
            m_phase_1 = row.phase_1
            m_phase_2 = row.phase_2
            m_phase_3 = row.phase_3
            m_id_model = row.id_model

            tmp11 = len(m_id_model)
            m_kolor_model, m_kod_model, m_comment_model, = [], [], []
            while tmp11 > 0:
                tmp11 -= 1
                id_model = m_id_model.pop(0)
                gr_model = session.query(directory_of_model).filter_by(
                    id_model=id_model).all()
                for row5 in gr_model:
                    m_kolor_model.append(row5.kolor_model)
                    m_kod_model.append(row5.kod_model)
                    m_comment_model.append(row5.comment_model)

            if len(list(m_quantity_pars_model)) == 1:
                m_quantity_pars_model = m_quantity_pars_model[0]
                # m_phase_1_model = m_phase_1_model[0]
                # m_phase_2_model = m_phase_2_model[0]
                # m_phase_3_model = m_phase_3_model[0]
                m_phase_1 = m_phase_1[0]
                m_phase_2 = m_phase_2[0]
                m_phase_3 = m_phase_3[0]
                m_kolor_model = m_kolor_model[0]
                m_kod_model = m_kod_model[0]
                m_comment_model = m_comment_model[0]
#
            id_client_2 = session.query(directory_of_client).filter_by(
                id_client=row.id_client).all()
            if (len(str(id_client_2))) < 3:
                return json.dumps({
                    "Помилка в записі клієнта - id:": row.id_order}), 500
            for row1 in id_client_2:
                m_phone_client = (row1.phone_client)
#
            id_recipient_1 = session.query(directory_of_client).filter_by(
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
###
            real_money_1 = session.query(func.sum(
                directory_of_payment.payment).label('my_sum')).filter_by(
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
                         "street_house_apartment": m_street_house_apartment,
                         "second_name_client": m_second_name_client,
                         "first_name_client": m_first_name_client}
            full_block.append(one_block)

    return json.dumps(full_block)
