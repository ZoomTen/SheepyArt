# Base
from flask import Blueprint, render_template, escape, url_for, abort, request

# Database entries
from sheepyart.app.models import User, Art
from sqlalchemy import func

# functions
from sheepyart.app.common import make_user_gallery

# Stuff
from sheepyart.sheepyart import conf

gallery = Blueprint('gallery', __name__)

gallery_entries = 5

@gallery.route('/user/<username>/gallery', methods=['GET'])
def view_gallery(username):
    user = User.query.filter(func.lower(User.username)
                             == func.lower(username)).first()
    offset = request.args.get('offset', 0, type=int)
    if user:
        actual_username = user.username
        display_name = user.dispname
        image_file = url_for('static', filename='avatar/' + user.avatar)

        gallery_stuff = make_user_gallery(user, num_entries=gallery_entries,
                                          sort_new=True,
                                          offset=int(offset))

        prevpage = None
        nextpage = None

        if offset > 0:
            pagecounter = (offset - gallery_entries) \
                          if ((offset - gallery_entries) > 0) \
                          else 0
            prevpage = url_for('gallery.view_gallery', username=username ) \
                       + f'?offset={ pagecounter }'

        if len(gallery_stuff) >= gallery_entries:
            nextpage = url_for('gallery.view_gallery', username=username ) \
                       + f'?offset={ offset + gallery_entries }'

        return render_template("gallery.haml",
                               dispname=escape(display_name),
                               username=escape(actual_username),
                               gallery_snips=gallery_stuff,
                               avatar=image_file,
                               ui_tab_selected=['','selected','',''],
                               prevpage=prevpage,
                               nextpage=nextpage
                               )
    abort(404)
