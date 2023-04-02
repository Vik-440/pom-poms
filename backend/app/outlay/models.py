from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.base_model import Base


class DB_outlay(Base):
    __tablename__ = 'directory_of_outlay'
    id_outlay = Column('id_outlay', Integer, primary_key=True)
    data_outlay = Column('data_outlay', Date)
    id_outlay_class = Column('id_outlay_class', String)
    money_outlay = Column('money_outlay', Integer)
    comment = Column('comment_outlay', String)

    # def to_json(self):
    #     outlay = {
    #         'id_outlay': self.id_outlay,
    #         'data_outlay': self.data_outlay,
    #         'id_outlay_class': self.id_outlay_class,
    #         'money_outlay': self.money_outlay,
    #         'comment': self.comment}
    #     return outlay