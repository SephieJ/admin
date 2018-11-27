# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms import DecimalField
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import Optional, Length


class ResourceForm(FlaskForm):
    name = StringField()
    description = StringField()
    image_url = FileField()
    price = DecimalField()
    location = StringField()
    resource_hour = StringField()
    quantity = IntegerField()
    keywords = TextAreaField()


class WishlistForm(FlaskForm):
    name = StringField(validators=[InputRequired('Wishlist name is required')])
    description = TextAreaField(validators=[InputRequired('Description name is required'), Length(min=0, max=250)])


class UpdateForm(FlaskForm):
    name = StringField()
    description = StringField()
    image_url = FileField()
    price = DecimalField()
    location = StringField()
    resource_hour = StringField()
    quantity = IntegerField()
    keywords = StringField()
