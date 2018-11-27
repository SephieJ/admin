
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class TicketForm(FlaskForm):
    reference_code = StringField()
    created_date = StringField()
    resource_ref_codes = StringField()
    issuer = StringField()
    message = StringField()
    status = StringField()
    solution = TextAreaField(validators=[InputRequired('Solution is required.')])

class TicketSupportForm(FlaskForm):
    reference_code = StringField()
    status = StringField()
    status = StringField()
    solution = TextAreaField()

class SupportChatForm(FlaskForm):
    message = StringField()
