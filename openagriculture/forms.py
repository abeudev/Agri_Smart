from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, EqualTo
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.widgets import HiddenInput

class CreateFieldForm(FlaskForm):

    name     = StringField(label='Field Name :', validators=[Length(min=4,max=25),DataRequired()])
    crop     = SelectField('Crop name :', choices=[('mais', 'Mais'), ('barley', 'Barley'), ('soybean', 'Soybean')], validators=[DataRequired()])
    geometry = HiddenField(label='Geometry :', validators=[Length(min=4, message="Define field geometry")])
    submit   = SubmitField(label='Save Field')

class DeleteFieldForm(FlaskForm):

    field              = SelectField(label='Field To Delete Name', validators=[DataRequired()])
    confirm_field_name = StringField(label='Confirm Name', validators=[DataRequired(), EqualTo('field')])
    submit             = SubmitField(label="Delete Field")
