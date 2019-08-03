# Base
from flask import Blueprint, render_template, escape, url_for, Response

# Database entries
from sheepyart.app.models import User, Art
from sqlalchemy import func

# functions
from sheepyart.app.common import make_user_gallery

# Stuff
from sheepyart.sheepyart import conf

gallery = Blueprint('gallery', __name__)


@gallery.route('/user/<username>/gallery', methods=['GET'])
def view_gallery(username):
    user = User.query.filter(func.lower(User.username)
                             == func.lower(username)).first()
    if user:
        actual_username = user.username
        display_name = user.dispname
        image_file = url_for('static', filename='avatar/' + user.avatar)

        gallery_stuff = make_user_gallery(user, num_entries=10, sort_new=True)

        return render_template("gallery.haml",
                               dispname=escape(display_name),
                               username=escape(actual_username),
                               gallery_snips=gallery_stuff,
                               avatar=image_file,
                               ui_tab_selected=['','selected','','']
                               )
    return Response(status=404)
