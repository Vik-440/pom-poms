from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class MaterialForm(FlaskForm):
    name_color = StringField('name_color', validators=[DataRequired(), Length(min=2, max=50)])
    # article = StringField('article', validators=[DataRequired(), Length(min=2, max=50)])
    width_color = IntegerField('width_color', validators=[DataRequired(), NumberRange(min=0)])
    thickness_color = IntegerField('thickness_color', validators=[DataRequired(), NumberRange(min=0)])
    bab_quantity_color = IntegerField('bab_quantity_color', validators=[DataRequired(), NumberRange(min=0)])
    bab_weight_color = IntegerField('bab_weight_color', validators=[DataRequired(), NumberRange(min=0)])
    weight_color = IntegerField('weight_color', validators=[DataRequired(), NumberRange(min=0)])
    manufacturer_color = StringField('manufacturer_color', validators=[DataRequired()])
    reserve_color = IntegerField('reserve_color', validators=[DataRequired(), NumberRange(min=0)])
    weight_10m_color = IntegerField('weight_10m_color', validators=[DataRequired(), NumberRange(min=0)])
    comment_color = StringField('comment_color', validators=[DataRequired(), Length(min=0, max=50)])


# {'color_new': 0, 'name_color': 'new for test', 'width_color': 50, 'bab_quantity_color': 1, 
#  'weight_color': 1111, 'comment_color': 'only test', 'thickness_color': 36, 
#  'bab_weight_color': 130, 'manufacturer_color': 'Viktor', 'reserve_color': 0, 'weight_10m_color': 25}