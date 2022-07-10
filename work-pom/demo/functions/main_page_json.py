import json
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import directory_of_order, directory_of_client
from db.models import directory_of_group, directory_of_payment
from db.models import directory_of_model
from db.models import engine


def return_data_from_main_page(asked):
    with Session(engine) as session:
        if 'fulfilled_id_order' in asked:
            id_order = asked['fulfilled_id_order']
            fulfilled_order = asked['fulfilled_order']
            rows = session.query(directory_of_order).filter_by(
                id_order=id_order).update(
                    {'fulfilled_order': fulfilled_order})
            session.commit()
            one_block = {"id_order": "ok"}
            return json.dumps(one_block)
        # if 'phase_id_order' in asked:
        #     id_order=asked['phase_id_order']
        #     phase_1_model=asked['phase_1_model']
        #     phase_2_model=asked['phase_2_model']
        #     phase_3_model=asked['phase_3_model']
        #     rows=session.query(directory_of_group).filter_by(id_order=id_order
        #         ).update({'phase_1_model':phase_1_model,'phase_2_model':phase_2_model,'phase_3_model':phase_3_model})
        #     session.commit()
        #     one_block = {"phase_id_order": "ok"}
        #     return json.dumps(one_block)

        id_order, comment_order, data_order, kolor_model, kod_model, \
            comment_model, quantity_pars_model, phase_1_model, phase_2_model, \
            phase_3_model, sum_payment, real_money, phone_client, \
            phone_recipient, sity, data_plane_order, fulfilled_order, \
            np_number, zip_code, street_house_apartment, second_name_client, \
            first_name_client = [], [], [], [], [], [], [], [], [], [], [], \
            [], [], [], [], [], [], [], [], [], [], []
        one_blok, full_block = [], []
        tmp_kolor_model, tmp_kod_model, tmp_comment_model, \
            tmp_quantity_pars_model, tmp_phase_1_model, \
            tmp_phase_2_model, tmp_phase_3_model = [], [], [], [], [], [], []

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
        # else: fulfilled_order_1='FALSE'#false
        if 'phone_client' in asked:
            phone_client_tmp = str(asked['phone_client'])
            id_client_1 = session.query(directory_of_client).filter_by(
                phone_client=phone_client_tmp).all()
            for row0 in id_client_1:
                id_client3 = row0.id_client
        if 'phone_client' in asked:
            if 'fulfilled_order' in asked:
                if fulfilled_order:
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
        else:
            id_order_1 = session.query(directory_of_order).filter(
                directory_of_order.data_order >= data_start,
                directory_of_order.data_order <= data_end).filter_by(
                fulfilled_order='FALSE').order_by('id_order').all()
        for row in id_order_1:
            id_order.append(row.id_order)
            comment_order.append(row.comment_order)
            data_order.append(str(row.data_order))
            data_plane_order.append(str(row.data_plane_order))
            fulfilled_order.append(row.fulfilled_order)
            sum_payment.append(row.sum_payment - row.discont_order)
            id_group_1 = session.query(directory_of_group).filter_by(
                id_order=row.id_order).all()
            if (len(str(id_group_1))) < 3:
                return json.dumps({
                    "Помилка в записі клієнта (не має моделей у Group)-id:":
                    row.id_order}), 500
            tmp_kolor_model, tmp_kod_model, tmp_comment_model,\
                tmp_quantity_pars_model, tmp_phase_1_model, \
                tmp_phase_2_model, tmp_phase_3_model = [], [], [], [], [], [],\
                []
            for row1 in id_group_1:
                tmp_quantity_pars_model.append(row1.quantity_pars_model)
                tmp_phase_1_model.append(row1.phase_1_model)
                tmp_phase_2_model.append(row1.phase_2_model)
                tmp_phase_3_model.append(row1.phase_3_model)

                if row1.id_model is None:
                    return json.dumps({
                        "Відсутній запис моделі у Group - id:": row.id_order}
                        ), 500
                if row1.quantity_pars_model is None:
                    return json.dumps({
                        "Відсутня кількість пар у Group - id:": row.id_order}
                        ), 500

                id_model_1 = session.query(directory_of_model).filter_by(
                    id_model=row1.id_model).all()
                for row2 in id_model_1:
                    tmp_kolor_model.append(row2.kolor_model)
                    tmp_kod_model.append(row2.kod_model)
                    tmp_comment_model.append(row2.comment_model)

            if len(tmp_quantity_pars_model) == 1:
                tmp_quantity_pars_model = tmp_quantity_pars_model[0]
                tmp_phase_1_model = tmp_phase_1_model[0]
                tmp_phase_2_model = tmp_phase_2_model[0]
                tmp_phase_3_model = tmp_phase_3_model[0]
                tmp_kolor_model = tmp_kolor_model[0]
                tmp_kod_model = tmp_kod_model[0]
                tmp_comment_model = tmp_comment_model[0]

            quantity_pars_model.append(tmp_quantity_pars_model)
            phase_1_model.append(tmp_phase_1_model)
            phase_2_model.append(tmp_phase_2_model)
            phase_3_model.append(tmp_phase_3_model)
            kolor_model.append(tmp_kolor_model)
            kod_model.append(tmp_kod_model)
            comment_model.append(tmp_comment_model)
            id_client_2 = session.query(directory_of_client).filter_by(
                id_client=row.id_client).all()
            if (len(str(id_client_2))) < 3:
                return json.dumps({
                    "Помилка в записі клієнта - id:": row.id_order}), 500
            for row1 in id_client_2:
                phone_client.append(row1.phone_client)
            id_recipient_1 = session.query(directory_of_client).filter_by(
                id_client=row.id_recipient).all()
            if (len(str(id_recipient_1))) < 3:
                return json.dumps({
                    "Помилка в записі отримувача - id:": row.id_order}), 500
            for row1 in id_recipient_1:
                second_name_client.append(row1.second_name_client)
                first_name_client.append(row1.first_name_client)
                phone_recipient.append(row1.phone_client)
                np_number.append(row1.np_number)
                zip_code.append(row1.zip_code)
                street_house_apartment.append(row1.street_house_apartment)
                sity.append(row1.sity)

            real_money_1 = session.query(func.sum(
                directory_of_payment.payment).label('my_sum')).filter_by(
                id_order=row.id_order).first()
            real_money.append(real_money_1.my_sum)

        a1a = len(id_order)
        while a1a > 0:
            a1a -= 1
            el1 = id_order.pop(0)
            el2 = comment_order.pop(0)
            el3 = data_order.pop(0)
            el4 = kolor_model.pop(0)
            el5 = kod_model.pop(0)
            el6 = comment_model.pop(0)
            el7 = quantity_pars_model.pop(0)
            el8 = phase_1_model.pop(0)
            el9 = phase_2_model.pop(0)
            el10 = phase_3_model.pop(0)
            el11 = sum_payment.pop(0)
            el12 = real_money.pop(0)
            el13 = phone_client.pop(0)
            el14 = phone_recipient.pop(0)
            el15 = sity.pop(0)
            el16 = data_plane_order.pop(0)
            el17 = fulfilled_order.pop(0)
            el18 = np_number.pop(0)
            el19 = zip_code.pop(0)
            el20 = street_house_apartment.pop(0)
            el21 = second_name_client.pop(0)
            el22 = first_name_client.pop(0)

            one_block = {"id_order": el1, "comment_order": el2,
                         "data_order": el3, "kolor_model": el4,
                         "kod_model": el5, "comment_model": el6,
                         "quantity_pars_model": el7, "phase_1_model": el8,
                         "phase_2_model": el9, "phase_3_model": el10,
                         "sum_payment": el11, "real_money": el12,
                         "phone_client": el13, "phone_recipient": el14,
                         "sity": el15, "data_plane_order": el16,
                         "fulfilled_order": el17, "np_number": el18,
                         "zip_code": el19, "street_house_apartment": el20,
                         "second_name_client": el21, "first_name_client": el22}
            full_block.append(one_block)
    return json.dumps(full_block)