# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms.validators import InputRequired
from wtforms.validators import Optional

class InvitationForm(FlaskForm):
    email_category = SelectField(validators=[InputRequired('Email Category is required')])
    emails = TextAreaField(validators=[InputRequired('Email is required')])
    # BCC = TextAreaField(validators=[InputRequired('BCC is required')])
class CSVEmailForm(FlaskForm):
    csvfile = FileField(validators=[Optional()])
