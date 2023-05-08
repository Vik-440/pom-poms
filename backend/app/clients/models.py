from sqlalchemy import Column, Integer, String
from app.base_model import Base


class DB_client(Base):
    __tablename__ = 'directory_of_client'
    id_client = Column('id_client', Integer, primary_key=True)
    phone = Column('phone_client', String, unique=True)
    second_name = Column('second_name_client', String)
    first_name = Column('first_name_client', String)
    surname = Column('surname_client', String)
    city = Column('sity', String)
    np_number = Column('np_number', Integer)
    team = Column('team', String)
    coach = Column('coach', String)
    zip_code = Column('zip_code', Integer)
    address = Column('street_house_apartment', String)
    comment = Column('comment_client', String)
