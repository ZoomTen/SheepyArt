'''
    Login route. This also handles logouts.
'''
# Base
from flask import Blueprint, render_template

# Additional functions
from flask import flash, redirect, url_for, request

# Form functions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms_components import DateRange

# User model
from sheepyart.app.models import User
from sqlalchemy import func

# Login functions
from flask_login import login_user, current_user, logout_user

# Crypt functions
from flask_bcrypt import Bcrypt
hash = Bcrypt()

# Logging
from sheepyart.sheepyart import app

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)

class SiteWideLoginForm(FlaskForm):
    'SheepyArt site-wide login form object. has no validation.'

    # User details
    username = StringField('Username')

    password = PasswordField('Password')

    submit = SubmitField('Login')

class LoginForm(FlaskForm):
    'SheepyArt login form object.'

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
    stay = BooleanField('Remember this login')
    submit = SubmitField('Login')

@login.route('/login', methods=['GET', 'POST'])
def do_login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('browse.do_browse'))
    else:
        if request.method == "POST":
            if form.validate_on_submit():
                # FIXME: Add email input functionality
                user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()

                if user:
                    check_pw = hash.check_password_hash(user.password, form.password.data)
                    if check_pw:
                        login_user(user, remember=form.stay.data)

                        # LOG: User log in.
                        app.logger.info(f"User '{user.username}' (ID:'{user.id}') has logged in.")

                        flash(f"Logged in as '{ form.username.data }'!", 'success')

                        target = request.args.get('next')
                        if target:
                            return redirect(target)
                        else:
                            return redirect(url_for('browse.do_browse'))
                    else:
                        flash('Login failed, check your password!', 'error')

                else:
                    flash('Login failed, check your username!', 'error')
                return render_template("login.haml", form=form)

            for field, errors in form.errors.items():
                for err in errors:
                    flash(err, 'error')
            return render_template("login.haml", form=form)

        else:
            return render_template("login.haml", form=form)

@logout.route('/logout', methods=['GET', 'POST'])
def do_logout():
    logout_uname = (current_user.username, current_user.id)
    logout_user()

    # LOG: User log out.
    app.logger.info(f"User '{logout_uname[0]}' (ID:'{logout_uname[1]}') has logged out.")

    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('browse.do_browse'))
