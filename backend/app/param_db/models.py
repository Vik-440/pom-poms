from sqlalchemy import Column, Integer, String
from app.base_model import Base


class ParamDb(Base):
    """parameters which saved in postgres DB"""
    __tablename__ = 'parameter_db'
    parameter_id = Column('parameter_id', Integer, primary_key=True)
    parameter_name = Column('parameter_name', String, unique=True)
    parameter_str = Column('parameter_str', String, default=None)
    parameter_int = Column('parameter_int', Integer, default=None)
    parameter_description = Column(
        'parameter_description', String, default=None)
