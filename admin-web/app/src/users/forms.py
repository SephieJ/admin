# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
# from wtforms import PasswordField
from wtforms import DateField
# from wtforms.validators import InputRequired
# from wtforms.validators import Optional


class UserForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    email = StringField()
    birtdate = DateField()
    landline_number = StringField()
    mobile_number = StringField()
    roles = StringField()
    email = StringField()
