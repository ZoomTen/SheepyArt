# Base
from flask import Blueprint, render_template
from flask import flash, request
from flask_login import login_required, current_user

# Form functions
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, BooleanField
from wtforms import SelectField, TextAreaField, RadioField, FileField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError
from wtforms_components import DateRange

# Database entries
from sheepart.sheepart import db, app
from sheepart.app.models import Art

# Database functions
from sqlalchemy import func

# Image functions
import secrets
from os import path

# Thumbnailing
# FIXME: Try using the imagemagick modules
from PIL import Image

upload = Blueprint('upload', __name__)

class UploadForm(FlaskForm):
    'Sheepart upload form object.'

    # User details
    title = StringField('Art Title',
                           [
                               InputRequired('Please enter a title')
                           ])
    # FIXME: Change category field to a combobox.
    category = StringField('Category',
                           [
                               InputRequired('Please enter a category')
                           ])
    tags = StringField('Tags',
                           [
                               InputRequired('Please enter some tags')
                           ])
    image = FileField('Image file',
                           [
                               FileRequired('Please choose an image file'),
                               FileAllowed(['jpg', 'png', 'gif'])
                           ])
    description = TextAreaField('Description')

    has_nsfw = RadioField(label='Mature Content?',
                           validators=[
                               InputRequired('Please enter a mature rating level')
                           ],
                           choices=[
                                ('0', 'No'),
                                ('1', 'Yes'),
                                ('2', 'Yes (strict)')
                           ])

    license = SelectField(label='License',
                          validators=[
                               InputRequired('Please select a license')
                           ],
                           choices=[
                                ('0', 'All rights reserved'),
                                ('1', 'CC BY-NC 4.0'),
                                ('2', 'CC BY 4.0'),
                                ('3', 'CC BY-NC-ND 4.0'),
                                ('4', 'CC BY-ND .0'),
                                ('5', 'CC BY-NC-SA 4.0'),
                                ('6', 'CC BY-SA 4.0'),
                                ('7', 'Public Domain')
                           ])
    agree_tos = BooleanField('Agree to terms?',
                             validators=[
                                 InputRequired('You must agree to the terms.')
                             ])

    submit = SubmitField('Submit Art')

def upload_art_image(form_art):
    hex = secrets.token_hex(8)
    name, ext = path.splitext(form_art.filename)

    new_name = hex + ext
    finalpath = path.join(app.root_path, 'static', 'uploads', new_name)

    thumb_ext = 'jpg'
    thumb_name = hex + '_thumb.' + thumb_ext
    thumbpath = path.join(app.root_path, 'static', 'thumbnail', thumb_name)

    form_art.save(finalpath)

    thumbsize = (150, 150)
    with Image.open(form_art) as orig:
        rgb = orig.convert('RGB')
        rgb.thumbnail(thumbsize, Image.ANTIALIAS)
        rgb.save(thumbpath)

    return (finalpath, thumbpath)


@upload.route('/upload', methods=['GET', 'POST'])
@login_required
def do_upload():
    form = UploadForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # FIXME: don't use a test return
            # FIXME: Add to the art database
            test_return = '<h1>Test</h1>'

            if form.image.data:
                image_file = upload_art_image(form.image.data)
                test_return += f"<p>Uploaded to: '{image_file[0]}'</p>"
                test_return += f"<p>Thumbnailed to: '{image_file[1]}'</p>"

            test_return += f"<p>Title: '{form.title.data}'</p>"
            test_return += f"<p>Category:'{form.category.data}'</p>"
            test_return += f"<p>Tags:'{form.tags.data}'"
            test_return += f"<p>File:'{form.image.data.filename}'</p>"
            test_return += f"<p>NSFW:'{form.has_nsfw.data}'</p>"
            test_return += f"<p>License:'{form.license.data}'</p>"

            return test_return
        for field, errors in form.errors.items():
            for err in errors:
                flash(err, 'error')
        return render_template("upload.haml", form=form)
    else:
        return render_template("upload.haml", form=form)
