from sqlalchemy import Column, Integer, String
from app.base_model import Base


class DB_product(Base):
    __tablename__ = 'directory_of_model'
    id_product = Column('id_model', Integer, primary_key=True)
    article = Column('kod_model', String, unique=True)
    colors = Column('kolor_model', String)
    price = Column('price_model', Integer)
    id_color_1 = Column('id_color_1', Integer)
    part_1 = Column('id_color_part_1', Integer)
    id_color_2 = Column('id_color_2', Integer)
    part_2 = Column('id_color_part_2', Integer)
    id_color_3 = Column('id_color_3', Integer)
    part_3 = Column('id_color_part_3', Integer)
    id_color_4 = Column('id_color_4', Integer)
    part_4 = Column('id_color_part_4', Integer)
    comment = Column('comment_model', String)
        