import json
from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import directory_of_order, directory_of_client
from db.models import directory_of_group, directory_of_payment
from db.models import directory_of_model
from db.models import engine
import datetime


with Session(engine) as session:
    a1a = 0
    my_list, tmp1, tmp2, tmp3, tmp4 = [], [], [], [], []
    while a1a < 71:
        my_list.append(a1a)
        a1a += 1
    my_list_2 = my_list[:]
#
    q1 = (datetime.datetime.now())
#
    result_list = session.query(directory_of_order).filter(
        directory_of_order.id_order.in_(my_list)).order_by('id_order').all()
    for row in result_list:
        # print(row)
        tmp1.append(str(row.data_order))
        tmp2.append(row.id_order)
#
    q2 = (datetime.datetime.now())
#
    result_list = select(directory_of_order).where(
        directory_of_order.id_order.in_(my_list)).order_by('id_order')
    www = session.scalars(result_list)
    for row in www:
        tmp3.append(str(row.data_order))
        tmp4.append(row.id_order)
    q3 = (datetime.datetime.now())
#
    print(datetime.datetime.now())
    q = len(tmp3)
    k = 0
    while k < q:
        print(tmp4[k], " - ", tmp3[k])
        k += 1
    print("---------------------------------")
    q = len(tmp1)
    k = 0
    while k < q:
        print(tmp2[k], " - ", tmp1[k])
        k += 1
    print("---------------------------------")
    print(q2-q1)
    print(q3-q2)
    # print(q2-q1-q3+q2)
