from sqlalchemy import null
from _2_new_order_page import return_data_from_order_page, return_data_from_client, return_data_from_kod
from _2_new_order_page import return_data_from_full_kod, return_data_from_full_person, return_data_from_final_order
import json
from sqlalchemy import create_engine,  MetaData, true, text, Integer, String, Table, Column, and_, or_
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, session, mapper, declarative_base#, decl_base, decl_api
from sqlalchemy.ext.declarative import declarative_base
from data_pompom_create import directory_of_order, directory_of_client, directory_of_team, directory_of_model
from data_pompom_create import directory_of_group, directory_of_payment, directory_of_sity, directory_of_color
from data_pompom_create import directory_of_outlay, directory_of_outlay_class
from data_pompom_create import engine


Session = sessionmaker(engine)
Session.configure(bind=engine)
session = Session()

def return_data_from_material(search):
    # data = return_data_from_order_page()
    # id_new_order = data['id_new_order']
    # time_last_order = data['time_last_order']
    # data_comeback= {'id_new_order':id_new_order, 'time_last_order':time_last_order}
    data_material={"testdata" : "Test-GET-OK"}
    return json.dumps(data_material, ensure_ascii=False)
