# Base
from flask import Blueprint
from flask import render_template
from flask_login import current_user

# Database entries
from sheepyart.sheepyart import app
from sheepyart.app.models import Art, Category

# Date conversion
from datetime import datetime as dt
from os import path

# Markdown tingz
from sheepyart.app.common import parse_markdown

art = Blueprint('art', __name__)


@art.route('/art/<art_id>', methods=['GET'])
def view_art(art_id):
    art_view = Art.query.get(art_id)

    if art_view:
        by = art_view.by

        published = dt.strftime(art_view.pubdate, '%B %-d, %Y (UTC)')

        description = parse_markdown(art_view.description)

        # FIXME: art: humanize file sizes
        filesize = path.getsize(path.join(app.root_path,
                                          'static', 'uploads', art_view.image)
                                )

        cat = Category.query.get(art_view.category)
        if cat.parent_id is not None:
            par_cat = Category.query.get(cat.parent_id)

            return render_template('art.haml', art=art_view, by=by,
                                   published=published, filesize=filesize,
                                   description=description,
                                   user=current_user,
                                   cat=(par_cat, cat)
                                   )

        return render_template('art.haml', art=art_view, by=by,
                               published=published,
                               filesize=filesize, description=description,
                               user=current_user,
                               cat=(cat)
                               )
    return render_template('art.haml')
