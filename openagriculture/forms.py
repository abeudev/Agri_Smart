from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, EqualTo, Email
from wtforms import StringField, SubmitField, SelectField, HiddenField, PasswordField
from wtforms.widgets import HiddenInput

################################################################################

class RegisterForm(FlaskForm):

    username      = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1     = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2     = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit        = SubmitField(label='Create Account')

################################################################################

class LoginForm(FlaskForm):
    username = StringField(label="User Name: ", validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit   = SubmitField(label='Sign in')

################################################################################

class EditUserDetailsForm(FlaskForm):

    company_name    = StringField(label="Company Name", validators=[DataRequired()])
    farm_address    = StringField(label="Farm Address", validators=[DataRequired()])
    fiscal_code     = StringField(label="Fiscal Code", validators=[DataRequired()])
    submit          = SubmitField(label='Submit')

################################################################################

class CreateFieldForm(FlaskForm):

    name     = StringField(label='Field Name :', validators=[Length(min=4,max=25),DataRequired()])
    crop     = SelectField('Crop name :', choices=[('mais', 'Mais'), ('barley', 'Barley'), ('soybean', 'Soybean')], validators=[DataRequired()])
    geometry = HiddenField(label='Geometry :', validators=[Length(min=4, message="Define field geometry")])
    submit   = SubmitField(label='Save Field')

################################################################################

class DeleteFieldForm(FlaskForm):

    field              = SelectField(label='Field To Delete Name', validators=[DataRequired()])
    confirm_field_name = StringField(label='Confirm Name', validators=[DataRequired(), EqualTo('field')])
    submit             = SubmitField(label="Delete Field")

################################################################################
