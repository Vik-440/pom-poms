from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.base_model import Base


class DB_payment(Base):
    __tablename__ = 'directory_of_payment'
    id_payment = Column('id_payment', Integer, primary_key=True)
    id_order = Column('id_order', Integer, ForeignKey(
        'directory_of_order.id_order'))
    payment = Column('payment', Integer)
    method_payment = Column('metod_payment', String)
    data_payment = Column('data_payment', Date)

    # def to_json(self):
    #     payment = {
    #         'id_payment': self.id_payment,
    #         'id_order': self.id_order,
    #         'payment': self.payment,
    #         'method_payment': self.method_payment,
    #         'data_payment': self.data_payment}
    #     return payment
