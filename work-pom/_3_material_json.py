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
    # with Session(engine) as session:
        j_id_color=[]
        j_name_color=[]
        j_width_color=[]
        j_bab_quantity_color=[]
        j_weight_color=[]
        j_comment_color=[]

        if search ==999 or search==0:
            if search == 999:
                None
                material_1=session.query(directory_of_color).all()
            elif search == 0:
                None
                material_1=session.query(directory_of_color).filter(directory_of_color.weight_color > 0).all()
            for row in material_1:
                j_id_color.append(row.id_color)
                j_name_color.append(row.name_color)
                j_width_color.append(row.width_color)
                j_bab_quantity_color.append(row.bab_quantity_color)
                j_weight_color.append(row.weight_color)
                j_comment_color.append(row.comment_color)
            a1a=len(j_id_color)
            print(a1a)
            full_block=[]
            while a1a > 0:
                a1a-=1
                element_1=j_id_color[0]
                del j_id_color[0]
                element_2=j_name_color[0]
                del j_name_color[0]
                element_3=j_width_color[0]
                del j_width_color[0]
                element_4=j_bab_quantity_color[0]
                del j_bab_quantity_color[0]
                element_5=j_weight_color[0]
                del j_weight_color[0]
                element_6=j_comment_color[0]
                del j_comment_color[0]

                one_block = {"id_color": element_1, "name_color": element_2, "width_color" : element_3,
                    "bab_quantity_color" : element_4, "weight_color" : element_5, "comment_color" : element_6}

                full_block.append(one_block)
        # data_material={"testdata" : "Test-GET-OK"}
        return json.dumps(full_block)       #, ensure_ascii=False
