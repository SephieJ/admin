# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
# from wtforms import SelectField
from wtforms import FileField
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import Optional


class CategoryForm(FlaskForm):
    name = StringField(validators=[InputRequired('Category Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])
    image = FileField(validators=[Optional()])


class SubCategoryForm(FlaskForm):
    name = StringField(validators=[InputRequired('SubCategory Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])


class SuggestedCategoryForm(FlaskForm):
    name = StringField(validators=[InputRequired('Category Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])
    image = FileField(validators=[Optional()])


class SuggestedSubcategoryForm(FlaskForm):
    name = StringField(validators=[InputRequired('Category Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])
