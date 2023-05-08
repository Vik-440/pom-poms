from sqlalchemy import Column, Integer, String, Numeric
from app.base_model import Base


class DB_materials(Base):
    __tablename__ = 'directory_of_color'
    id_material = Column('id_color', Integer, primary_key=True)
    name = Column('name_color', String, unique=True)
    article = Column('kod_color', String, unique=True)
    width = Column('width_color', Integer)
    thickness = Column('thickness_color', Integer)
    spool_qty = Column('bab_quantity_color', Integer)
    spool_weight = Column('bab_weight_color', Integer)
    weight = Column('weight_color', Integer)
    manufacturer = Column('manufacturer_color', String)
    reserve = Column('reserve_color', Integer)
    weight_10m = Column('weight_10m_color', Numeric(scale=2))
    comment = Column('comment_color', String)
