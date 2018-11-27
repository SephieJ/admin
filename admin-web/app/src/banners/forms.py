from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import FileField
from wtforms.validators import InputRequired


class BannersForm(FlaskForm):
    name = StringField(validators=[InputRequired('Banner Type is required')])
    description = TextAreaField(validators=[InputRequired('Description is required')])


class ImagesForm(FlaskForm):
    name = StringField(validators=[InputRequired('Banner Type is required')])
    image = FileField(validators=[InputRequired('Image is required')])
    image_link = StringField(validators=[InputRequired('Image link is required')])
