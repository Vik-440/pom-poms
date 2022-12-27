# from unittest import result
# from sqlalchemy import select
# from sqlalchemy import true, update
# from sqlalchemy import func
# from datetime import datetime
# from sqlalchemy.orm import Session
# from db.models import directory_of_order
# from db.models import directory_of_client, directory_of_payment
# from db.models import directory_of_model
# from db.models import engine
# import datetime
# import json
# from flask import jsonify, request

number = 123456
xxx = sum([int(x) for x in str(number)])
# yyy = lambda x: for x in xxx
print(xxx)

# import calendar
# from datetime import datetime, timedelta
# ds = datetime.today()
# ds1 = ds.strftime('%Y-%m-%d')
# dsy = int(ds.strftime('%Y'))
# dsm = int(ds.strftime('%m'))
# print(dsy, dsm)
# data_start_sql = datetime.today().replace(day=1).strftime('%Y-%m-%d')
# data_end_sql = datetime.today().replace(day=(
#     calendar.monthrange(dsy, dsm)[1])).strftime('%Y-%m-%d')
# print(data_start_sql, data_end_sql)

# data_start_sql = (((datetime.today()).replace(day=1)-timedelta(
#     days=1))).replace(day=1).strftime('%Y-%m-%d')
# data_end_sql = ((datetime.today()).replace(
#         day=1)-timedelta(days=1)).strftime('%Y-%m-%d')
# print(data_start_sql, data_end_sql)
# # this year
# data_start_sql = ds.replace(month=1, day=1).strftime('%Y-%m-%d')
# data_end_sql = ds.replace(month=12, day=31).strftime('%Y-%m-%d')
# print(data_start_sql, data_end_sql)

# days_year = (ds-ds.replace(month=1, day=1))
# forecast = round((5555/days_year.days)*365)
# print(days_year, forecast)

# from routes.main import return_data_from_flask
# from routes.main import tmp_test_tmp
# from routes.main import ret_dat_fin_pay_get
# y = ret_dat_fin_pay_get()
# x = tmp_test_tmp()
# print(ret_dat_fin_pay_get())
# print(y)
# a = json.loads(y)
# print(a)


# with Session(engine) as session:
#     r_list = select(directory_of_order.id_order).order_by(
#         'id_order')
#     id_list = session.execute(r_list)
#     n_order = 0
#     for row in id_list:
#         id_order = int(row.id_order)
#         if id_order < 2000:
#             n_order += 1
#             phase1_list, phase2_list, phase3_list = [], [], []
#             q_pos = []
#             list_from_group = select(
#                 directory_of_order.quantity_pars_model,
#                 directory_of_order.fulfilled_order).filter_by(
#                 id_order=id_order)
#             q_list = session.execute(list_from_group)
#             for row1 in q_list:
#                 q_pos = row1.quantity_pars_model
#                 fulfilled_order = row1.fulfilled_order
#             len_pos = len(q_pos)
#             for x in range(len_pos):
#                 if fulfilled_order is True:
#                     phase1_list.append(0)
#                     phase2_list.append(0)
#                     phase3_list.append(0)
#                 else:
#                     phase1_list.append(q_pos[x] * 2)
#                     phase2_list.append(q_pos[x] * 2)
#                     phase3_list.append(q_pos[x] * 2)

#             session.query(directory_of_order).filter(
#                 directory_of_order.id_order == id_order).update(
#                 {"phase_1": (phase1_list),
#                  "phase_2": (phase2_list),
#                  "phase_3": (phase3_list)})
#             session.commit()
#             print(n_order, " - order №_", id_order, " is fixed")


# with Session(engine) as session:
#     r_list = select(directory_of_order.id_order).order_by(
#         'id_order')
#     id_list = session.execute(r_list)
#     for row in id_list:
#         id_order = int(row.id_order)
#         if id_order < 2000:

#             id_model_list, quantity_pars_model_list = [], []
#             price_model_order_list, phase_model_list = [], []
#             phase_model_list1, phase_model_list2 = [], []
#             phase_model_list3 = []
#             # test = [1, 2, 3, 4]
#             list_from_group = select(
#                 directory_of_group.id_model,
#                 directory_of_group.quantity_pars_model,
#                 directory_of_group.phase_1_model,
#                 directory_of_group.phase_2_model,
#                 directory_of_group.phase_3_model,
#                 directory_of_group.price_model_order).filter_by(
#                 id_order=id_order).order_by('id_group_model')
#             group_list = session.execute(list_from_group)
#             for row1 in group_list:
#                 id_model_list.append(row1.id_model)
#                 quantity_pars_model_list.append(row1.quantity_pars_model)
#                 phase_model_list1.append(row1.phase_1_model)
#                 phase_model_list2.append(row1.phase_2_model)
#                 phase_model_list3.append(row1.phase_3_model)
#                 price_model_order_list.append(row1.price_model_order)
#             # print(id_order, " - ", id_model_list, quantity_pars_model_list,
#             # phase_model_list1, phase_model_list2, phase_model_list3,
#             # price_model_order_list)

#             session.query(directory_of_order).filter(
#                 directory_of_order.id_order == id_order).update(
#                 {"id_model": (id_model_list),
#                     "quantity_pars_model": (quantity_pars_model_list),
#                     "phase_1_model": (phase_model_list1),
#                     "phase_2_model": (phase_model_list2),
#                     "phase_3_model": (phase_model_list3),
#                     "price_model_order": (price_model_order_list)})
#             session.commit()
#            # print(id_order, "- is saved")
#            # s1, s2, s3, s4, s5, s6 = [], [], [], [], [], []
#            # download = select(
#            #     directory_of_order.id_model,
#            #     directory_of_order.quantity_pars_model,
#            #     directory_of_order.phase_1_model,
#            #       directory_of_order.phase_2_model,
#            #     directory_of_order.phase_3_model,
#            #       directory_of_order.price_model_order).filter_by(
#            #     id_order = id_order).order_by('id_order')
#            # order_list = session.execute(download)
#            # for row1 in order_list:
#            #     s1 = ((row1.id_model))
#            #     s2 = (row1.quantity_pars_model)
#            #     s3 = (row1.phase_1_model)
#            #     s4 = (row1.phase_2_model)
#            #     s5 = (row1.phase_3_model)
#            #     s6 = (row1.price_model_order)
#            #    # print(id_order, " - ", s1, s2, s3, s4, s5, s6)
#            #    # print(s1[0], s3[1])


# with Session(engine) as session:
#     r_list = select(directory_of_group.id_group_model).order_by(
#         'id_group_model')
#     id_l = session.execute(r_list)
#     for row in id_l:
#         id = int(row.id_group_model)
#         print("id_group:", id, "is OK")
#         session.query(directory_of_group).filter_by(
#             id_group_model=id).update({'phase_1_model': True,
#                                        'phase_2_model': True,
#                                        'phase_3_model': True})
#         session.commit()


# with Session(engine) as session:
#     data_start = "2022-04-01"
#     data_end = "2022-07-01"
#     cancel_order = 0
#     id_1 = session.query(directory_of_order).filter(
#         directory_of_order.data_order >= data_start,
#         directory_of_order.data_order <= data_end).order_by(
#         'id_order').all()
#     for row in id_1:
#         id = row.id_order
#         sum = int(row.sum_payment)
#         dis = int(row.discont_order)
#         data = row.data_order

#         rm = session.query(func.sum(
#             directory_of_payment.payment).label('my_sum')).filter_by(
#             id_order=row.id_order).first()
#         rmoney = (rm.my_sum)
#         if rmoney is None:
#             rmoney = 0
#         pay = (sum - dis - rmoney)

#         if pay != 0:
#             print(id, " - ", data, " - ", pay, " - iban")

#             session.query(directory_of_order).filter_by(
#                 id_order=id).update({'fulfilled_order': True})
#             ins = directory_of_payment(
#                 id_order=id,
#                 metod_payment="iban",
#                 payment=pay,
#                 data_payment=data)
#             session.add(ins)
#             session.commit()
#         else:
#             cancel_order += 1
#     print("canseled order: ", cancel_order)


# ins = directory_of_model(
#                     kod_model=data_from_new_page['kod_model'],
#                     id_color_1=int(data_from_new_page['id_color_1']),
#                     id_color_part_1=int(data_from_new_page['id_color_part_1']),
#                     id_color_2=int(data_from_new_page['id_color_2']),
#                     id_color_part_2=int(data_from_new_page['id_color_part_2']),
#                     id_color_3=int(data_from_new_page['id_color_3']),
#                     id_color_part_3=int(data_from_new_page['id_color_part_3']),
#                     id_color_4=int(data_from_new_page['id_color_4']),
#                     id_color_part_4=int(data_from_new_page['id_color_part_4']),
#                     price_model=data_from_new_page['price_model'],
#                     comment_model=data_from_new_page['comment_model'],
#                     kolor_model=data_from_new_page['kolor_model'])
#             session.add(ins)
#             session.commit()


# with Session(engine) as session:
#     a1a = 0
#     my_list, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6 = [], [], [], [], [], [], []
#     while a1a < 71:
#         my_list.append(a1a)
#         a1a += 1
#     # my_list_2 = my_list[:]
#     my_list = [3, 1, 2, 3, 1, 2]
# #
#     q1 = (datetime.datetime.now())
# #
#     result_list = session.query(directory_of_order).filter(
#         directory_of_order.id_order.in_(my_list)).order_by('id_order').all()
#     for row in result_list:
#         # print(row)
#         tmp1.append(str(row.data_order))
#         tmp2.append(row.id_order)
# #
#     q2 = (datetime.datetime.now())
# #
#     result_list = select(directory_of_order).where(
#         directory_of_order.id_order.in_(my_list))
#     www = session.scalars(result_list)
#     for row in www:
#         tmp3.append(str(row.data_order))
#         tmp4.append(row.id_order)
#     q3 = (datetime.datetime.now())
# #
#     result_list = session.query(directory_of_order).filter(
#         directory_of_order.id_order.in_(my_list)).order_by('id_order').all()
#     for row in result_list:
#         # print(row)
#         tmp5.append(str(row.data_order))
#         tmp6.append(row.id_order)
# #
#     q4 = (datetime.datetime.now())
#     print(datetime.datetime.now())
#     # q = len(tmp3)
#     # k = 0
#     # while k < q:
#     #     print(tmp4[k], " - ", tmp3[k])
#     #     k += 1
#     print("---------------------------------")
#     q = len(tmp3)
#     k = 0
#     while k < q:
#         print(tmp4[k], " - ", tmp3[k])
#         k += 1
#     print("---------------------------------")
#     # q = len(tmp5)
#     # k = 0
#     # while k < q:
#     #     print(tmp6[k], " - ", tmp5[k])
#     #     k += 1
#     # print("---------------------------------")
#     print(my_list)
#     print("input - ", len(my_list), " =-|-= output - ", len(tmp4))
#     print(q2-q1)
#     print(q3-q2)
#     print(q4-q3)
#     # print(q2-q1-q3+q2)#


# ins = directory_of_model(
#                     kod_model=data_from_new_page['kod_model'],
#                     id_color_1=int(data_from_new_page['id_color_1']),
#                     id_color_part_1=int(data_from_new_page['id_color_part_1']),
#                     id_color_2=int(data_from_new_page['id_color_2']),
#                     id_color_part_2=int(data_from_new_page['id_color_part_2']),
#                     id_color_3=int(data_from_new_page['id_color_3']),
#                     id_color_part_3=int(data_from_new_page['id_color_part_3']),
#                     id_color_4=int(data_from_new_page['id_color_4']),
#                     id_color_part_4=int(data_from_new_page['id_color_part_4']),
#                     price_model=data_from_new_page['price_model'],
#                     comment_model=data_from_new_page['comment_model'],
#                     kolor_model=data_from_new_page['kolor_model'])
#             session.add(ins)
#             session.commit()

# ins = directory_of_model(
#                     kod_model=data_from_new_page['kod_model'],
#                     id_color_1=int(data_from_new_page['id_color_1']),
#                     id_color_part_1=int(data_from_new_page['id_color_part_1']),
#                     id_color_2=int(data_from_new_page['id_color_2']),
#                     id_color_part_2=int(data_from_new_page['id_color_part_2']),
#                     id_color_3=int(data_from_new_page['id_color_3']),
#                     id_color_part_3=int(data_from_new_page['id_color_part_3']),
#                     id_color_4=int(data_from_new_page['id_color_4']),
#                     id_color_part_4=int(data_from_new_page['id_color_part_4']),
#                     price_model=data_from_new_page['price_model'],
#                     comment_model=data_from_new_page['comment_model'],
#                     kolor_model=data_from_new_page['kolor_model'])
#             session.add(ins)
#             session.commit()
