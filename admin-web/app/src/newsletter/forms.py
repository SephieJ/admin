from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms.validators import InputRequired
from wtforms.validators import Optional

class NewsletterForm(FlaskForm):
    email_category = SelectField(validators=[InputRequired('Email Category is required')])
    emails = StringField(validators=[InputRequired('Email is required')])
    # BCC = TextAreaField(validators=[InputRequired('BCC is required')])