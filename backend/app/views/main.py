from flask import request, Blueprint
from app import db
import json
import datetime
from ..models.directories import directory_of_order as db_o
from ..models.directories import directory_of_client as db_c
from ..models.directories import directory_of_payment as db_p
from ..models.directories import directory_of_model as db_m
from ..utils.exception_decorator import log_decorator


main_blueprint = Blueprint("main", __name__)


@log_decorator()
@main_blueprint.route('/', methods=['GET'])
def main():
    """Preparing main page with or without same requests"""
    if request.method == 'GET':
        data = request.args
        data_finish_search = datetime.today().strftime('%Y-%m-%d')
        data_start_search = '2016-01-01'
        fulfilled = str('False')
        if 'data_start' in data:
            data_start_search = data['data_start']
        if 'data_finish' in data:
            data_finish_search = data['data_finish']
        if 'fulfilled' in data:
            fulfilled = data['fulfilled']
#
        id_client_list, id_model_list = [], []
        if 'phone_client' in data:
            phone_client = data['phone_client']
            stmt = db.select(db_c.id_client)\
                .where(db_c.phone_client == phone_client)\
                .order_by(db_c.id_client)
            id_client_list.append(db.session.execute(stmt).scalar())
        elif 'id_client' in data:
            id_client = data['id_client']
            stmt = db.select(db_c.id_client)\
                .where(db_c.id_client == id_client)\
                .order_by(db_c.id_client)
            id_client_list.append(db.session.execute(stmt).scalar())
        elif 'team' in data:
            team = data['team']
            stmt = db.select(db_c.id_client)\
                .where(db_c.team == team).order_by(db_c.id_client)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_client_list.append(row)
        elif 'coach' in data:
            coach = data['coach']
            stmt = db.select(db_c.id_client)\
                .where(db_c.coach == coach).order_by(db_c.id_client)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_client_list.append(row)
        elif 'city' in data:
            city = data['city']
            stmt = db.select(db_c.id_client)\
                .where(db_c.sity == city).order_by(db_c.id_client)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_client_list.append(row)

        if 'kod_model' in data:
            kod_model = data['kod_model']
            stmt = db.select(db_m.id_model)\
                .where(db_m.kod_model == kod_model).order_by(db_m.id_model)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_model_list.append(row)
        elif 'kod_model_like' in data:
            kod_model_like = data['kod_model_like']
            look_for_similar = ('%' + str(kod_model_like) + '%')
            stmt = db.select(db_m.id_model)\
                .where(db_m.kod_model.like(look_for_similar))\
                .order_by(db_m.id_model)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_model_list.append(row)
        elif 'kolor_like' in data:
            kolor_model_like = data['kolor_like']
            look_for_similar = ('%' + str(kolor_model_like) + '%')
            stmt = db.select(db_m.id_model)\
                .where(db_m.kolor_model.like(look_for_similar))\
                .order_by(db_m.id_model)
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_model_list.append(row)
        id_order_list = []
        for id_model_cucle in id_model_list:
            stmt = db.select(db_o.id_order)\
                .where(db_o.id_model.any(id_model_cucle))
            pre_list = db.session.execute(stmt).scalars()
            for row in pre_list:
                id_order_list.append(row)
        select_modul = db.select(
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
                    db.or_(
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
                    db.and_(
                        db_o.id_order.in_(id_order_list),
                        db.or_(
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
                    db.or_(
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
                    db.and_(
                        db_o.id_order.in_(id_order_list),
                        db.or_(
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

        list_order = db.session.execute(stmt).all()

        if not list_order:
            stmt = db.select(db.func.max(db_o.id_order))
            last_order = db.session.execute(stmt).scalar_one()
            stmt = select_modul.where(db_o.id_order == last_order)
            list_order = db.session.execute(stmt).all()

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

            m_kolor_model, m_kod_model, m_comment_model, = [], [], []

            for id_model in m_id_model:
                stmt = db.select(
                    db_m.kolor_model, db_m.kod_model, db_m.comment_model)\
                    .where(db_m.id_model == id_model)
                gr_model = db.session.execute(stmt).all()
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

            id_client_2 = db.session.query(db_c).filter_by(
                id_client=row.id_client).all()
            if (len(str(id_client_2))) < 3:
                return json.dumps({
                    "Помилка в записі клієнта - id:": row.id_order}), 500
            for row1 in id_client_2:
                m_phone_client = (row1.phone_client)

            id_recipient_1 = db.session.query(db_c).filter_by(
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

            real_money_1 = db.session.query(db.func.sum(
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
    else:
        return {"request_metod": "error"}, 500