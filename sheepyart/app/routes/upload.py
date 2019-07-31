# Base
from flask import Blueprint, render_template
from flask import flash, request, redirect, url_for
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
from sheepyart.sheepyart import db, app
from sheepyart.app.models import Art, Category

# Database functions
from sqlalchemy import func

# Image functions
import secrets
from os import path

# Thumbnailing
# FIXME: Try using the imagemagick modules
from PIL import Image

# Logging
from sheepyart.sheepyart import app

upload = Blueprint('upload', __name__)

upload_categories = Category.query.filter(Category.parent_id != None)

categories_list = []

try:
    for cat in upload_categories:
        cur_id = cat.id
        par_id = cat.parent_id
        par = Category.query.filter(Category.id == par_id and Category.parent_id == None).first()
        categories_list.append( (str(cur_id), f"{par.title}/{cat.title}") )
except:
    pass

class UploadForm(FlaskForm):
    'SheepyArt upload form object.'

    # User details
    title = StringField('Art Title',
                           [
                               InputRequired('Please enter a title')
                           ])
    # FIXME: Change category field to a combobox.
    category = SelectField('Category',
                           validators=[
                               InputRequired('Please enter a category')
                           ],
                           choices=categories_list)
    tags = StringField('Tags',
                           [
                               InputRequired('Please enter some tags')
                           ])
    image = FileField('Image file',
                           [
                               FileRequired('Please choose an image file'),
                               FileAllowed(['jpg', 'png', 'gif'])
                           ])
    description = TextAreaField('Description or Contents')

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

    return (new_name, thumb_name)


@upload.route('/upload', methods=['GET', 'POST'])
@login_required
def do_upload():
    form = UploadForm()

    if request.method == "POST":
        if form.validate_on_submit():
            by = (current_user.username, current_user.id)

            if form.image.data:
                image_file = upload_art_image(form.image.data)
                uploaded_art = Art(title=form.title.data,
                                   image=image_file[0],
                                   thumbnail=image_file[1],
                                   user_id=by[1],
                                   description=form.description.data,
                                   tags=form.tags.data,
                                   category=int(form.category.data),
                                   nsfw=int(form.has_nsfw.data),
                                   license=int(form.license.data)
                                   )
            else:
                uploaded_art = Art(title=form.title.data,
                                   user_id=by[1],
                                   description=form.description.data,
                                   tags=form.tags.data,
                                   category=int(form.category.data),
                                   nsfw=int(form.has_nsfw.data),
                                   license=int(form.license.data)
                                   )

            db.session.add(uploaded_art)
            db.session.commit()

            # LOG: Image upload
            app.logger.info(f"User '{by[0]}' (ID: '{by[1]}') uploaded '{form.title.data}', assigned ID (insert ID)")

            flash('Your art has been uploaded!', 'success')
            # FIXME: upload: redirect to art page
            return redirect(url_for('browse.do_browse'))

        for field, errors in form.errors.items():
            for err in errors:
                flash(err, 'error')
        return render_template("upload.haml", form=form)
    else:
        return render_template("upload.haml", form=form)
