import json
from unittest import result
from sqlalchemy import select, true
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import directory_of_order, directory_of_client
from db.models import directory_of_group, directory_of_payment
from db.models import directory_of_model
from db.models import engine
import datetime


with Session(engine) as session:
    r_list = select(directory_of_group.id_group_model).order_by(
        'id_group_model')
    id_l = session.execute(r_list)
    for row in id_l:
        id = int(row.id_group_model)
        print("id_group:", id, "is OK")
        session.query(directory_of_group).filter_by(
            id_group_model=id).update({'phase_1_model': True,
                                       'phase_2_model': True,
                                       'phase_3_model': True})
        session.commit()


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
#                     kod_model=data_from_new_page['kod_model'],    # int for all
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
