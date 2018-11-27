# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class FaqsForm(FlaskForm):
    name = StringField(validators=[InputRequired('FAQ Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])
    # image_url = FileField(validators=[Optional()])


class QuestionsForm(FlaskForm):
    question = StringField(validators=[InputRequired('Question is required')])
    # response = StringField(validators=[InputRequired('Response is required')])
    response = TextAreaField(validators=[InputRequired('Response is required')])
