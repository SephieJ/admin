# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms import PasswordField
from wtforms import DateField
from wtforms import SelectField
from wtforms.validators import InputRequired, EqualTo
from wtforms.validators import Optional

class AdminForm(FlaskForm):
    first_name = StringField(validators=[InputRequired('First Name is required')])
    last_name = StringField(validators=[InputRequired('Last Name is required')])
    landline_number = StringField(validators=[Optional()])
    mobile_number = StringField(validators=[Optional()])
    designation = StringField(validators=[Optional()])
    #birth_date = StringField(validators=[InputRequired('Birthdate is required')])
    email = StringField(validators=[InputRequired('Email Address is required')])
    username = StringField(validators=[InputRequired('Username is required')])
    password = PasswordField(validators=[InputRequired('Password is required')])
    roles = SelectField(u'Choose Role', choices=[('', '--SELECT--'), ('ADMIN', 'ADMIN')], validators=[InputRequired('Roles is required')])
    image = FileField(validators=[Optional()])


class UpdateForm(FlaskForm):
    first_name = StringField(validators=[InputRequired('First Name is required')])
    last_name = StringField(validators=[InputRequired('Last Name is required')])
    landline_number = StringField(validators=[Optional()])
    mobile_number = StringField(validators=[Optional()])
    designation = StringField(validators=[Optional()])
    #birth_date = StringField(validators=[Optional()])
    email = StringField(validators=[InputRequired('Email Address is required')])
    roles = SelectField(u'Choose Role', choices=[('', '--SELECT--'), ('ADMIN', 'ADMIN')], validators=[InputRequired('Roles is required')])
    image = FileField(validators=[Optional()])


class ChangePasswordForm(FlaskForm):
    old_password = StringField(validators=[InputRequired('Old password is required')])
    new_password = StringField(validators=[InputRequired('New password is required')])
    confirm_password = StringField(validators=[InputRequired('Confirm password is required'), EqualTo('new_password', message='Passwords must match.')])
