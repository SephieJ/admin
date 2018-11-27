# -*- coding: utf-8 -*-

import bleach
import os
import string
import random
import requests
from flask import flash, current_app as app
from werkzeug.utils import secure_filename
from app.src.utils import constants
from wtforms.validators import ValidationError

def special_chars():
    message = 'Special characters are not allowed.'

    def _special_chars(form, field):
        invalidChars = string.punctuation
        word = field.data
        if any(char in invalidChars for char in word):
            raise ValidationError(message)

    return _special_chars

def sg_mobile_number():
    message = 'Wrong format for mobile number.'

    def _sg_mobile_number(form, field):
        mobile_number = field.data
        if not mobile_number.startswith(('8', '9')):
            raise ValidationError(message)

    return _sg_mobile_number


def sg_office_number():
    message = 'Wrong format for office number.'

    def _sg_office_number(form, field):
        office_number = field.data
        if not office_number.startswith(('6')):
            raise ValidationError(message)

    return _sg_office_number

def sanitize(inputs):
    sanitized = {}
    for item in inputs:
        sanitized[item] = str(inputs[item])
        # Check if the data is int or float since bleach convert numeric to string.
        if isinstance(inputs[item], (int, float)) is True:
            sanitized[item] = inputs[item]
        else:
            sanitized[item] = bleach.clean(str(inputs[item])).strip()
    return sanitized


def flash_errors(form):
    # Flashes form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload(image):
    if image and allowed_file(image.filename):
        # Make the filename safe, remove unsupported characters
        image_name = secure_filename(image.filename)
        # Move the file from the temporal folder to the upload folder we set up
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        return constants.IMAGE_UPLOAD_DIR + image_name
