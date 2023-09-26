from sqlalchemy import Date, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects import postgresql
from app.base_model import Base


class DB_orders(Base):
    __tablename__ = 'directory_of_order'
    id_order = Column('id_order', Integer, primary_key=True)
    date_create = Column('data_order', Date)
    date_plane_send = Column('data_plane_order', Date)
    id_client = Column('id_client', Integer, ForeignKey(
        'directory_of_client.id_client'))
    id_recipient = Column('id_recipient', Integer, ForeignKey(
        'directory_of_client.id_client'))
    status_order = Column('fulfilled_order', Boolean)
    sum_payment = Column('sum_payment', Integer)
    discount = Column('discont_order', Integer)
    comment = Column('comment_order', String)
    id_models = Column('id_model', postgresql.ARRAY(Integer))
    qty_pars = Column('quantity_pars_model', postgresql.ARRAY(Integer))
    price_model_sell = Column('price_model_order', postgresql.ARRAY(Integer))
    phase_1 = Column('phase_1', postgresql.ARRAY(Integer))
    phase_2 = Column('phase_2', postgresql.ARRAY(Integer))
    phase_3 = Column('phase_3', postgresql.ARRAY(Integer))
