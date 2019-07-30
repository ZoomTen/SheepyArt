# Base
from flask import Blueprint, render_template, escape

# Database entries
from sheepart.app.models import User
from sqlalchemy import func

userpage = Blueprint('userpage', __name__)


@userpage.route('/user/<username>', methods=['GET'])
def view_userpage(username):
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if user:
        actual_username = user.username
        return render_template("userpage.haml", username=escape(actual_username))
    else:
        return render_template("userpage.haml")
