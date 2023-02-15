import json
from datetime import datetime
from sqlalchemy import func, select, or_, and_, join, table
from sqlalchemy.orm import Session, aliased
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
            elif 'city' in got_request:
                city = got_request['city']
                stmt = select(db_c.id_client)\
                    .where(db_c.sity == city).order_by(db_c.id_client)
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
                    .where(db_m.kod_model.ilike(look_for_similar))\
                    .order_by(db_m.id_model)
                pre_list = session.execute(stmt).scalars()
                for row in pre_list:
                    id_model_list.append(row)
            elif 'kolor_model_like' in got_request:
                kolor_model_like = got_request['kolor_model_like']
                look_for_similar = ('%' + str(kolor_model_like) + '%')
                stmt = select(db_m.id_model)\
                    .where(db_m.kolor_model.ilike(look_for_similar))\
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
            client_alias = aliased(db_c)
            recipient_alias = aliased(db_c)
               
            select_modul = (select(
                func.sum(db_p.payment).label('my_sum'),
                # func.array_agg(db_m.kod_model).label('cod_model'),
                db_o.id_order,
                db_o.comment_order,
                db_o.data_order,
                db_o.data_plane_order,
                db_o.fulfilled_order,
                db_o.sum_payment,
                db_o.discont_order,
                db_o.quantity_pars_model,
                db_o.phase_1,
                db_o.phase_2,
                db_o.phase_3,
                db_o.id_model,
                client_alias.phone_client.label('phone_order'),
                recipient_alias.second_name_client,
                recipient_alias.first_name_client,
                recipient_alias.phone_client,
                recipient_alias.np_number,
                recipient_alias.zip_code,
                recipient_alias.street_house_apartment,
                recipient_alias.sity)
                .group_by(
                    db_o,
                    client_alias,
                    recipient_alias
                )
                .join(client_alias, db_o.id_client == client_alias.id_client)
                .join(recipient_alias, db_o.id_recipient == recipient_alias.id_client)
                .join(db_p, db_o.id_order == db_p.id_order)
                # .join(db_m, db_o.id_model == db_m.id_model)
                )

            select_modul = select_modul.where(
                                db_o.data_order >= data_start_search,
                                db_o.data_order <= data_finish_search
                )

            if fulfilled == 'all':
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list)))\
                        .order_by(db_o.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                       db_o.id_order.in_(id_order_list))\
                        .order_by(db_o.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        and_(
                            db_o.id_order.in_(id_order_list),
                            or_(
                                db_o.id_client.in_(id_client_list),
                                db_o.id_recipient.in_(id_client_list))))\
                        .order_by(db_o.id_order)
                else:
                    stmt = select_modul.order_by(db_o.id_order)
                    # where(
                        # db_o.data_order >= data_start_search,
                        # db_o.data_order <= data_finish_search)\
                        # .order_by(db_o.id_order)
            else:
                if id_client_list and not id_order_list:
                    stmt = select_modul.where(
                        db_o.fulfilled_order == fulfilled,
                        or_(
                            db_o.id_client.in_(id_client_list),
                            db_o.id_recipient.in_(id_client_list)))\
                        .order_by(db_o.id_order)
                elif id_order_list and not id_client_list:
                    stmt = select_modul.where(
                        db_o.fulfilled_order == fulfilled,
                        db_o.id_order.in_(id_order_list))\
                        .order_by(db_o.id_order)
                elif id_order_list and id_client_list:
                    stmt = select_modul.where(
                        db_o.fulfilled_order == fulfilled,
                        and_(
                            db_o.id_order.in_(id_order_list),
                            or_(
                                db_o.id_client.in_(id_client_list),
                                db_o.id_recipient.in_(id_client_list))))\
                        .order_by(db_o.id_order)
                else:
                    if fulfilled == 'true':
                        stmt = select_modul.where(
                            db_o.fulfilled_order == fulfilled)\
                            .order_by(db_o.id_order)
                    else:
                        stmt = (select_modul
                            .where(db_o.fulfilled_order == fulfilled)
                            .order_by(db_o.data_plane_order))

            list_order = session.execute(stmt).all()

            if not list_order:
                stmt = select(func.max(db_o.id_order))
                last_order = session.execute(stmt).scalar_one()
                stmt = select_modul.where(db_o.id_order == last_order)
                list_order = session.execute(stmt).all()
#
            full_block = []
            for row in list_order:
                id_order = row.id_order
                comment_order = row.comment_order
                data_order = (str(row.data_order))
                data_plane_order = (str(row.data_plane_order))
                fulfilled_order = (row.fulfilled_order)
                sum_payment = (row.sum_payment - row.discont_order)
                quantity_pars_model = (row.quantity_pars_model)
                phase_1 = row.phase_1
                phase_2 = row.phase_2
                phase_3 = row.phase_3
                id_model = row.id_model
                phone_client = row.phone_order
                second_name_client = row.second_name_client
                first_name_client = row.first_name_client
                phone_recipient = row.phone_client
                np_number = row.np_number
                zip_code = row.zip_code
                street_house_apartment = row.street_house_apartment
                sity = row.sity
                real_money = row.my_sum
#
                kolor_model, kod_model, comment_model, = [], [], []

                for id_model in id_model:
                    stmt = select(
                        db_m.kolor_model, db_m.kod_model, db_m.comment_model)\
                        .where(db_m.id_model == id_model)
                    gr_model = session.execute(stmt).all()
                    for row5 in gr_model:
                        kolor_model.append(row5.kolor_model)
                        kod_model.append(row5.kod_model)
                        comment_model.append(row5.comment_model)
                        # print(id_model, row5.kolor_model, row5.kod_model, row5.comment_model)

                if len(list(quantity_pars_model)) == 1:
                    quantity_pars_model = quantity_pars_model[0]
                    phase_1 = phase_1[0]
                    phase_2 = phase_2[0]
                    phase_3 = phase_3[0]
                    kolor_model = kolor_model[0]
                    kod_model = kod_model[0]
                    comment_model = comment_model[0]
#

                one_block = {
                    "id_order": id_order,
                    "comment_order": comment_order,
                    "data_order": data_order,
                    "kolor_model": kolor_model,
                    "kod_model": kod_model,
                    "comment_model": comment_model,
                    "quantity_pars_model": quantity_pars_model,
                    "phase_1": phase_1,
                    "phase_2": phase_2,
                    "phase_3": phase_3,
                    "sum_payment": sum_payment,
                    "real_money": real_money,
                    "phone_client": phone_client,
                    "phone_recipient": phone_recipient,
                    "sity": sity,
                    "data_plane_order": data_plane_order,
                    "fulfilled_order": fulfilled_order,
                    "np_number": np_number,
                    "zip_code": zip_code,
                    "street_house_apartment": street_house_apartment,
                    "second_name_client": second_name_client,
                    "first_name_client": first_name_client
                    }
                full_block.append(one_block)
        # print(full_block)
        return json.dumps(full_block)
    except Exception as e:
        return json.dumps(f'Error in function main: {e}')
