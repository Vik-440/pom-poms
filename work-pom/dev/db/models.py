from sqlalchemy import Date, ForeignKey, Numeric, create_engine, Column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("PSQL_URL")
Base = declarative_base()


class directory_of_order(Base):
    __tablename__ = 'directory_of_order'
    id_order = Column('id_order', Integer, primary_key=True)
    data_order = Column('data_order', Date)
    data_plane_order = Column('data_plane_order', Date)
    id_client = Column('id_client', Integer, ForeignKey(
        'directory_of_client.id_client'))
    id_recipient = Column('id_recipient', Integer, ForeignKey(
        'directory_of_client.id_client'))
    data_send_order = Column('data_send_order', Date)
    fulfilled_order = Column('fulfilled_order', Boolean)
    sum_payment = Column('sum_payment', Integer)
    discont_order = Column('discont_order', Integer)
    comment_order = Column('comment_order', String)

    client = relationship("directory_of_client", foreign_keys=[id_client])


class directory_of_client(Base):
    __tablename__ = 'directory_of_client'
    id_client = Column('id_client', Integer, primary_key=True)
    phone_client = Column('phone_client', String)
    second_name_client = Column('second_name_client', String)
    first_name_client = Column('first_name_client', String)
    surname_client = Column('surname_client', String)
    sity = Column('sity', String)
    np_number = Column('np_number', Integer)
    team = Column('team', String)
    coach = Column('coach', String)
    zip_code = Column('zip_code', Integer)
    street_house_apartment = Column('street_house_apartment', String)
    comment_client = Column('comment_client', String)


class directory_of_model(Base):
    __tablename__ = 'directory_of_model'
    id_model = Column('id_model', Integer, primary_key=True)
    kod_model = Column('kod_model', String)
    kolor_model = Column('kolor_model', String)
    price_model = Column('price_model', Integer)
    id_color_1 = Column('id_color_1', Integer)
    id_color_part_1 = Column('id_color_part_1', Integer)
    id_color_2 = Column('id_color_2', Integer)
    id_color_part_2 = Column('id_color_part_2', Integer)
    id_color_3 = Column('id_color_3', Integer)
    id_color_part_3 = Column('id_color_part_3', Integer)
    id_color_4 = Column('id_color_4', Integer)
    id_color_part_4 = Column('id_color_part_4', Integer)
    comment_model = Column('comment_model', String)


class directory_of_group(Base):
    __tablename__ = 'directory_of_group'
    id_group_model = Column('id_group_model', Integer, primary_key=True)
    id_model = Column('id_model', Integer)
    id_order = Column('id_order', Integer)
    quantity_pars_model = Column('quantity_pars_model', Integer)
    phase_1_model = Column('phase_1_model', Boolean)
    phase_2_model = Column('phase_2_model', Boolean)
    phase_3_model = Column('phase_3_model', Boolean)
    price_model_order = Column('price_model_order', Integer)


class directory_of_payment(Base):
    __tablename__ = 'directory_of_payment'
    id_payment = Column('id_payment', Integer, primary_key=True)
    id_order = Column('id_order', Integer, ForeignKey(
        'directory_of_order.id_order'))
    payment = Column('payment', Integer)
    metod_payment = Column('metod_payment', String)
    data_payment = Column('data_payment', Date)


class directory_of_color(Base):
    __tablename__ = 'directory_of_color'
    id_color = Column('id_color', Integer, primary_key=True)
    name_color = Column('name_color', String)
    kod_color = Column('kod_color', String)
    width_color = Column('width_color', Integer)
    thickness_color = Column('thickness_color', Integer)
    bab_quantity_color = Column('bab_quantity_color', Integer)
    bab_weight_color = Column('bab_weight_color', Integer)
    weight_color = Column('weight_color', Integer)
    manufacturer_color = Column('manufacturer_color', String)
    reserve_color = Column('reserve_color', Integer)
    weight_10m_color = Column('weight_10m_color', Integer)
    comment_color = Column('comment_color', String)


class directory_of_outlay(Base):
    __tablename__ = 'directory_of_outlay'
    id_outlay = Column('id_outlay', Integer, primary_key=True)
    data_outlay = Column('data_outlay', Date)
    id_outlay_class = Column('id_outlay_class', String)
    money_outlay = Column('money_outlay', Integer)
    quantity_outlay = Column('quantity_outlay', Numeric(8, 2))
    type_pc_outlay = Column('type_pc_outlay', String)
    comment_outlay = Column('comment_outlay', String)


class directory_of_outlay_class(Base):
    __tablename__ = 'directory_of_outlay_class'
    id_outlay_class = Column('id_outlay_class', Integer, primary_key=True)
    outlay_class = Column('outlay_class', String)


engine = create_engine(url)

Base.metadata.create_all(engine)
