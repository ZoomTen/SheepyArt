from flask import Blueprint
from flask import request, render_template

from flask import flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FormField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

register = Blueprint('register', __name__)


class RegistrationForm(FlaskForm):
    username = StringField(label='Username')
    password = PasswordField()
    dob = DateField('Date of Birth')
    agree_tos = BooleanField('Agree to terms?')
    submit = SubmitField('Sign Up')

@register.route('/register', methods=['GET', 'POST'])
def do_register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('browse.do_browse'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)
        return render_template("register.haml", mode='wtf', form=form)
