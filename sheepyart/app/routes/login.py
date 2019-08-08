'''
    Login route. This also handles logouts.
'''
# Base
from flask import Blueprint, render_template

# Additional functions
from flask import flash, redirect, url_for, request

# Form functions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length

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
    'SheepyArt site-wide login form object. Validation handled by login form.'
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

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter(func.lower(User.username)
                                     == func.lower(form.username.data)).first()\
                    or User.query.filter(func.lower(User.email)
                                        == func.lower(form.username.data)).first()

            if user:
                check_pw = hash.check_password_hash(user.password,
                                                    form.password.data
                                                    )
                if check_pw:
                    login_user(user, remember=form.stay.data)

                    # LOG: User log in.
                    app.logger.info(f"User {user.username} (ID:{user.id}) has logged in.")

                    flash(f"Logged in as {user.username}!", 'success')

                    target = request.args.get('next')
                    if target:
                        return redirect(target)

                    return redirect(url_for(
                                            'userpage.view_userpage',
                                            username=user.username
                                            )
                                   )
                flash('Login failed, check your password!', 'error')
            flash('Login failed, check your username!', 'error')

            return render_template("login.haml", form=form)

        for field, errors in form.errors.items():
            for err in errors:
                flash(err, 'error')
        return render_template("login.haml", form=form)

    return render_template("login.haml", form=form)


@logout.route('/logout', methods=['GET', 'POST'])
def do_logout():
    print(current_user)
    if current_user.is_authenticated:
        logout_uname = (current_user.username, current_user.id)
        logout_user()

        # LOG: User log out.
        app.logger.info(f"User {logout_uname[0]} (ID:{logout_uname[1]}) has logged out.")

        flash('You have been successfully logged out.', 'info')
    return redirect(url_for('browse.do_browse'))
