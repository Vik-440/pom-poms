from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.base_model import Base


class DB_outlay(Base):
    __tablename__ = 'directory_of_outlay'
    id_outlay = Column('id_outlay', Integer, primary_key=True)
    data_outlay = Column('data_outlay', Date)
    id_outlay_class = Column('id_outlay_class', String)
    money_outlay = Column('money_outlay', Integer)
    comment = Column('comment_outlay', String)
