from flask import Blueprint
from flask import render_template

from flask import flash, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms_components import DateRange

from datetime import date
from dateutil.relativedelta import relativedelta

from sheepart.sheepart import db
from sheepart.app.models import User

from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

hash = Bcrypt()

register = Blueprint('register', __name__)

class RegistrationForm(FlaskForm):
    'Sheepart registration form object.'

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
    confirm_password = PasswordField('Confirm password',
                                     [
                                         InputRequired('Enter the password a second time.'),
                                         EqualTo('password', 'Passwords must match!')
                                     ])

    dispname = StringField('Display name',
                           [
                               InputRequired('Please set a display name!')
                           ])

    email = EmailField('Email',
                       [
                           InputRequired('Enter a e-mail address'),
                           Email('Must be a valid e-mail address!')
                       ])
    confirm_email = EmailField('Confirm e-mail',
                               [
                                   InputRequired('Enter the e-mail address a second time.'),
                                   EqualTo('email', 'E-mail addresses must match!')
                               ])

    # Personal details
    gender = SelectField('Gender',
                         choices=[
                             ('2', 'Male'),
                             ('3', 'Female'),
                             ('1', 'Other'),
                             ('0', 'Non-identifying')
                         ], validators=[InputRequired('Select a gender')])

    dob = DateField('Date of Birth', default=date(2000,1,1),
                    validators=[
                        InputRequired('Set a DoB'),
                        DateRange(
                            min=date(1900,1,1),
                            max=date.today() - relativedelta(years=13)
                            )
                    ])

    # FIXME: Expand countries
    country = SelectField('Country',
                          choices=[
                              ( '1', 'United States'),
                              ( '2', 'Canada'),
                              ('20', 'Egypt'),
                              ('48', 'Poland'),
                              ('60', 'Malaysia'),
                              ('61', 'Australia'),
                              ('62', 'Indonesia'),
                              ('999', 'Not saying'),
                          ], validators=[InputRequired('Select a country')])

    agree_tos = BooleanField('Agree to terms?',
                             validators=[
                                 InputRequired('You must agree to the terms.')
                             ])

    submit = SubmitField('Sign Up')


@register.route('/register', methods=['GET', 'POST'])
def do_register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        dispname=form.dispname.data,
                        email=form.email.data,
                        password=hash.generate_password_hash(form.password.data),
                        dob=form.dob.data,
                        gender=int(form.gender.data),
                        country=int(form.country.data))

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint' in str(e.__cause__):
                # FIXME: find a better way to deal with handling IntegrityError
                user = User.query.filter_by(username=form.username.data).first()
                email = User.query.filter_by(email=form.email.data).first()
                if user is not None:
                    flash('That username is already taken...', 'error')
                if email is not None:
                    flash('That e-mail address is already taken... if you forgot your password, use the "Forgot Password" link!',
                          'error')
            else:
                flash(f'Registration failed: {e.__cause__}','error')
            return render_template("register.haml", form=form)

        # FIXME: Redirect to the user's profile page.
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('browse.do_browse'))

    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash(err, 'error')

        return render_template("register.haml", form=form)
