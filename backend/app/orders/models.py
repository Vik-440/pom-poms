from sqlalchemy import Date, Column, Integer, String, Boolean
from sqlalchemy.dialects import postgresql
from app.base_model import Base


class DB_orders(Base):
    __tablename__ = 'directory_of_order'
    id_order = Column('id_order', Integer, primary_key=True)
    data_create = Column('data_order', Date)
    data_plane_send = Column('data_plane_order', Date)
    id_client = Column('id_client', Integer)
    id_recipient = Column('id_recipient', Integer)
    status_order = Column('fulfilled_order', Boolean)
    sum_payment = Column('sum_payment', Integer)
    discont = Column('discont_order', Integer)
    comment = Column('comment_order', String)
    id_models = Column('id_model', postgresql.ARRAY(Integer))
    qty_pars = Column('quantity_pars_model', postgresql.ARRAY(Integer))
    price_model_sell = Column('price_model_order', postgresql.ARRAY(Integer))
    phase_1 = Column('phase_1', postgresql.ARRAY(Integer))
    phase_2 = Column('phase_2', postgresql.ARRAY(Integer))
    phase_3 = Column('phase_3', postgresql.ARRAY(Integer))

    def to_json(self):
        order = {
            'id_order': self.id_order,
            'data_create': self.data_create,
            'data_plane_send': self.data_plane_send,
            'id_client': self.id_client,
            'id_recipient': self.id_recipient,
            'status_order': self.status_order,
            'sum_payment': self.sum_payment,
            'discont': self.discont,
            'comment': self.comment,
            'id_models': self.id_models,
            'qty_pars': self.qty_pars,
            'price_model_sell': self.price_model_sell,
            'phase_1': self.phase_1,
            'phase_2': self.phase_2,
            'phase_3': self.phase_3}
        return order
    