from sqlalchemy import Column, Integer, String
from app.base_model import Base


class DB_product(Base):
    __tablename__ = 'directory_of_model'
    id_product = Column('id_model', Integer, primary_key=True)
    article = Column('kod_model', String, unique=True)
    colors = Column('kolor_model', String)
    price = Column('price_model', Integer)
    id_color_1 = Column('id_color_1', Integer)
    id_part_1 = Column('id_color_part_1', Integer)
    id_color_2 = Column('id_color_2', Integer)
    id_part_2 = Column('id_color_part_2', Integer)
    id_color_3 = Column('id_color_3', Integer)
    id_part_3 = Column('id_color_part_3', Integer)
    id_color_4 = Column('id_color_4', Integer)
    id_part_4 = Column('id_color_part_4', Integer)
    comment = Column('comment_model', String)
        
    def to_json(self):
        product = {
            'id_product': self.id_product,
            'article': self.article,
            'colors': self.colors,
            'price': self.price,
            'id_color_1': self.id_color_1,
            'id_part_1': self.id_part_1,
            'id_color_2': self.id_color_2,
            'id_part_2': self.id_part_2,
            'id_color_3': self.id_color_3,
            'id_part_3': self.id_part_3,
            'id_color_4': self.id_color_4,
            'id_part_4': self.id_part_4,
            'comment': self.comment}
        return product
