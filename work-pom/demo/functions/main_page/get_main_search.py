import json
from datetime import datetime
from sqlalchemy import func, select, or_, and_
from sqlalchemy.orm import Session
from db.models import directory_of_order as db_o
from db.models import directory_of_client as db_c
from db.models import directory_of_payment as db_p
from db.models import directory_of_model as db_m
from db.models import engine


def get_main(got_request):
    """Main block for download the base table on main WEB page"""
    try:
        with Session(engine) as session:
            data_finish_search = datetime.today().strftime('%Y-%m-%d')
            data_start_search = '2016-01-01'
            fulfilled = str('False')
            if 'data_start' in got_request:
                data_start_search = got_request['data_start']
            if 'data_finish' in got_request:
                data_finish_search = got_request['data_finish']
            if 'fulfilled' in got_request:
                fulfilled = got_request['fulfilled']
#
            id_client_list, id_model_list = [], []
            if 'phone_client' in got_request:
                phone_client = got_request['phone_client']
                stmt = select(db_c.id_client)\
                    .where(db_c.phone_client == phone_client)\
                    .order_by(db_c.id_client)
                id_client_list.append(session.execute(stmt).scalar())
            elif 'id_client' in got_request:
                id_client = got_request['id_client']
                stmt = select(db_c.id_client)\
                    .where(db_c.id_client == id_client)\
                    .order_by(db_c.id_client)
                id_client_list.append(session.execute(stmt).scalar())
            elif 'team' in got_request:
                team = got_request['team']
                stmt = select(db_c.id_client)\
                    .where(db_c.team == team).order_by(db_c.id_client)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
            elif 'coach' in got_request:
                coach = got_request['coach']
                stmt = select(db_c.id_client)\
                    .where(db_c.coach == coach).order_by(db_c.id_client)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
            elif 'sity' in got_request:
                sity = got_request['sity']
                stmt = select(db_c.id_client)\
                    .where(db_c.sity == sity).order_by(db_c.id_client)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_client_list.append(row)
#
            if 'kod_model' in got_request:
                kod_model = got_request['kod_model']
                stmt = select(db_m.id_model)\
                    .where(db_m.kod_model == kod_model).order_by(db_m.id_model)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
            elif 'kod_model_like' in got_request:
                kod_model_like = got_request['kod_model_like']
                look_for_similar = ('%' + str(kod_model_like) + '%')
                stmt = select(db_m.id_model)\
                    .where(db_m.kod_model.like(look_for_similar))\
                    .order_by(db_m.id_model)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
            elif 'kolor_like' in got_request:
                kolor_model_like = got_request['kolor_like']
                look_for_similar = ('%' + str(kolor_model_like) + '%')
                stmt = select(db_m.id_model)\
                    .where(db_m.kolor_model.like(look_for_similar))\
                    .order_by(db_m.id_model)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
# ###########################################################################
            id_order_list = []
            for id_model_cucle in id_model_list:
                stmt = select(db_o.id_order)\
                    .where(db_o.id_model.any(id_model_cucle))
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_order_list.append(row)
# ###########################################################################
            select_modul = select(
                db_o.id_order, db_o.comment_order, db_o.data_order,
                db_o.data_plane_order, db_o.fulfilled_order, db_o.sum_payment,
                db_o.discont_order, db_o.quantity_pars_model, db_o.phase_1,
                db_o.phase_2, db_o.phase_3, db_o.id_model, db_o.id_client,
                db_o.id_recipient)
            if fulfilled == 'all':
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list)))\
                        .order_by(db_o.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        db_o.id_order.in_(id_order_list))\
                        .order_by(db_o.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        and_(
                            db_o.id_order.in_(id_order_list),
                            or_(
                                db_o.id_client.in_(id_client_list),
                                db_o.id_recipient.in_(id_client_list))))\
                        .order_by(db_o.id_order)
                else:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search)\
                        .order_by(db_o.id_order)
            else:
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        db_o.fulfilled_order == fulfilled,
                        or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list)))\
                        .order_by(db_o.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        db_o.fulfilled_order == fulfilled,
                        db_o.id_order.in_(id_order_list))\
                        .order_by(db_o.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        db_o.data_order >= data_start_search,
                        db_o.data_order <= data_finish_search,
                        db_o.fulfilled_order == fulfilled,
                        and_(
                            db_o.id_order.in_(id_order_list),
                            or_(
                                db_o.id_client.in_(id_client_list),
                                db_o.id_recipient.in_(id_client_list))))\
                        .order_by(db_o.id_order)
                else:
                    if fulfilled:
                        stmt = select_modul.where(
                            db_o.data_order >= data_start_search,
                            db_o.data_order <= data_finish_search,
                            db_o.fulfilled_order == fulfilled)\
                            .order_by(db_o.id_order)
                    else:
                        stmt = select_modul.where(
                            db_o.data_order >= data_start_search,
                            db_o.data_order <= data_finish_search,
                            db_o.fulfilled_order == fulfilled)\
                            .order_by(db_o.data_plane_order)

            list_order = session.execute(stmt).all()

            if not list_order:
                stmt = select(func.max(db_o.id_order))
                last_order = session.execute(stmt).scalar_one()
                stmt = select_modul.where(db_o.id_order == last_order)
                list_order = session.execute(stmt).all()
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
#
                m_kolor_model, m_kod_model, m_comment_model, = [], [], []

                for id_model in m_id_model:
                    stmt = select(
                        db_m.kolor_model, db_m.kod_model, db_m.comment_model)\
                        .where(db_m.id_model == id_model)
                    gr_model = session.execute(stmt).all()
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
    except Exception as e:
        return json.dumps(f'Error in function main: {e}')
