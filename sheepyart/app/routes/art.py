# Base
from flask import Blueprint
from flask import render_template, request, escape
from flask_login import current_user

# Database entries
from sheepyart.sheepyart import app
from sheepyart.app.models import Art, Category

# Date conversion
from datetime import datetime as dt
from os import path

art = Blueprint('art', __name__)

# FIXME: art: make this functional
@art.route('/art/<art_id>', methods=['GET'])
def view_art(art_id):
    art = Art.query.get(art_id)
    if art:
        by = art.by
        cat = Category.query.get(art.category)
        published = dt.strftime(art.pubdate, '%B %-d, %Y (UTC)')
        # FIXME: art: only allow certain html tags in the desc and escape others. better yet, use markdown. also provide a preview.
        description = escape(art.description)
        # FIXME: art: humanize file sizes
        filesize = path.getsize(path.join(app.root_path, 'static', 'uploads', art.image))
        if cat.parent_id is not None:
            par_cat = Category.query.get(cat.parent_id)
            return render_template('art.haml', art=art, by=by,
                                   published=published, filesize=filesize,
                                   description=description,
                                   user=current_user,
                                   cat=(par_cat, cat)
                                  )
        return render_template('art.haml', art=art, by=by, published=published,
                               filesize=filesize, description=description,
                               user=current_user,
                               cat=(cat)
                              )

    else:
        return render_template('art.haml')
