# Base
from flask import Blueprint, render_template, escape, url_for

# Database entries
from sheepyart.app.models import User, Art
from sqlalchemy import func

# functions
from sheepyart.app.common import make_user_gallery

# Stuff
from sheepyart.sheepyart import conf

userpage = Blueprint('userpage', __name__)


@userpage.route('/user/<username>', methods=['GET'])
def view_userpage(username):
    user = User.query.filter(func.lower(User.username)
                             == func.lower(username)).first()
    if user:
        actual_username = user.username
        display_name = user.dispname
        image_file = url_for('static', filename='avatar/' + user.avatar)

        gender = conf['genders'][str(user.gender)]
        joindate = user.joindate

        gallery_count = Art.query.filter_by(by=user).count()
        gallery_stuff = make_user_gallery(user, num_entries=5, sort_new=True)

        return render_template("userpage.haml",
                               dispname=escape(display_name),
                               username=escape(actual_username),
                               gallery_count=gallery_count,
                               gallery_snips=gallery_stuff,
                               gender=gender,
                               joindate=joindate,
                               avatar=image_file
                               )
    else:
        return render_template("userpage.haml")
