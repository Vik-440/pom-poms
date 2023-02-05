from app import db


class directory_of_order(db.Model):
    __tablename__ = 'directory_of_order'
    id_order = db.Column('id_order', db.Integer, primary_key=True)
    data_order = db.Column('data_order', db.Date)
    data_plane_order = db.Column('data_plane_order', db.Date)
    id_client = db.Column('id_client', db.Integer)
    id_recipient = db.Column('id_recipient', db.Integer)
    fulfilled_order = db.Column('fulfilled_order', db.Boolean)
    sum_payment = db.Column('sum_payment', db.Integer)
    discont_order = db.Column('discont_order', db.Integer)
    comment_order = db.Column('comment_order', db.String)

    id_model = db.Column('id_model', db.postgresql.ARRAY(db.Integer))
    quantity_pars_model = db.Column(
        'quantity_pars_model', db.postgresql.ARRAY(db.Integer))
    price_model_order = db.Column('price_model_order', db.postgresql.ARRAY(db.Integer))
    phase_1 = db.Column('phase_1', db.postgresql.ARRAY(db.Integer))
    phase_2 = db.Column('phase_2', db.postgresql.ARRAY(db.Integer))
    phase_3 = db.Column('phase_3', db.postgresql.ARRAY(db.Integer))


class directory_of_client(db.Model):
    __tablename__ = 'directory_of_client'
    id_client = db.Column('id_client', db.Integer, primary_key=True)
    phone_client = db.Column('phone_client', db.String)
    second_name_client = db.Column('second_name_client', db.String)
    first_name_client = db.Column('first_name_client', db.String)
    surname_client = db.Column('surname_client', db.String)
    sity = db.Column('sity', db.String)
    np_number = db.Column('np_number', db.Integer)
    team = db.Column('team', db.String)
    coach = db.Column('coach', db.String)
    zip_code = db.Column('zip_code', db.Integer)
    street_house_apartment = db.Column('street_house_apartment', db.String)
    comment_client = db.Column('comment_client', db.String)


class directory_of_model(db.Model):
    __tablename__ = 'directory_of_model'
    id_model = db.Column('id_model', db.Integer, primary_key=True)
    kod_model = db.Column('kod_model', db.String)
    kolor_model = db.Column('kolor_model', db.String)
    price_model = db.Column('price_model', db.Integer)
    id_color_1 = db.Column('id_color_1', db.Integer)
    id_color_part_1 = db.Column('id_color_part_1', db.Integer)
    id_color_2 = db.Column('id_color_2', db.Integer)
    id_color_part_2 = db.Column('id_color_part_2', db.Integer)
    id_color_3 = db.Column('id_color_3', db.Integer)
    id_color_part_3 = db.Column('id_color_part_3', db.Integer)
    id_color_4 = db.Column('id_color_4', db.Integer)
    id_color_part_4 = db.Column('id_color_part_4', db.Integer)
    comment_model = db.Column('comment_model', db.String)


class directory_of_payment(db.Model):
    __tablename__ = 'directory_of_payment'
    id_payment = db.Column('id_payment', db.Integer, primary_key=True)
    id_order = db.Column('id_order', db.Integer, db.ForeignKey(
        'directory_of_order.id_order'))
    payment = db.Column('payment', db.Integer)
    metod_payment = db.Column('metod_payment', db.String)
    data_payment = db.Column('data_payment', db.Date)


class directory_of_color(db.Model):
    __tablename__ = 'directory_of_color'
    id_color = db.Column('id_color', db.Integer, primary_key=True)
    name_color = db.Column('name_color', db.String)
    kod_color = db.Column('kod_color', db.String)
    width_color = db.Column('width_color', db.Integer)
    thickness_color = db.Column('thickness_color', db.Integer)
    bab_quantity_color = db.Column('bab_quantity_color', db.Integer)
    bab_weight_color = db.Column('bab_weight_color', db.Integer)
    weight_color = db.Column('weight_color', db.Integer)
    manufacturer_color = db.Column('manufacturer_color', db.String)
    reserve_color = db.Column('reserve_color', db.Integer)
    weight_10m_color = db.Column('weight_10m_color', db.Integer)
    comment_color = db.Column('comment_color', db.String)


class directory_of_outlay(db.Model):
    __tablename__ = 'directory_of_outlay'
    id_outlay = db.Column('id_outlay', db.Integer, primary_key=True)
    data_outlay = db.Column('data_outlay', db.Date)
    id_outlay_class = db.Column('id_outlay_class', db.String)
    money_outlay = db.Column('money_outlay', db.Integer)
    comment_outlay = db.Column('comment_outlay', db.String)