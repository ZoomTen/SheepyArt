# Base
from flask import Blueprint, render_template, request

# Form functions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms_components import DateRange

login = Blueprint('login', __name__)

class LoginForm(FlaskForm):
    'Sheepart login form object.'

    # User details
    username = StringField('Username',
                           [
                               InputRequired('Please enter a username'),
                               Length(min=2, max=20)
                           ])

    password = PasswordField('Password',
                             [
                                 InputRequired('Enter a password'),
                             ])

    submit = SubmitField('Login')

@login.route('/login', methods=['GET', 'POST'])
def do_login():
    form = LoginForm()

    if request.method == "POST":
        return render_template("login.haml", form=form)
    else:
        return render_template("login.haml", form=form)
