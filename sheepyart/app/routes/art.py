# Base
from flask import Blueprint
from flask import render_template
from flask_login import current_user

# Database entries
from sheepyart.sheepyart import app, db
from sheepyart.app.models import Art, Category, View, CollectionData, CollectionMeta

# Date conversion
from datetime import datetime as dt
from os import path

# Markdown tingz
from sheepyart.app.common import parse_markdown

# Humanization
from humanize import naturalsize

# Resolution
from PIL import Image

art = Blueprint('art', __name__)


@art.route('/art/<art_id>', methods=['GET'])
def view_art(art_id):
    art_view = Art.query.get(art_id)

    if art_view:
        # FIXME: art: viewing in this way is likely going to be a disaster
        isviewed_data = View(art_id=art_view.id)
        try:
            db.session.add(isviewed_data)
            db.session.commit()
        except:
            pass
        viewcount = View.query.filter_by(art_id=art_view.id).count()
        #
        by = art_view.by

        published = dt.strftime(art_view.pubdate, '%B %-d, %Y (UTC)')

        description = parse_markdown(art_view.description)

        in_collections = CollectionData.query.filter_by(art_id=art_id)
        favorites_count = 0

        for collection in in_collections.all():
            if CollectionMeta.query.get(collection.collection_id).use_as_favorites is True:
                favorites_count += 1

        collection_count = in_collections.count() - favorites_count

        favorited = None
        if current_user.is_authenticated:
            favstable = CollectionMeta.query.filter_by(user_id=current_user.id, use_as_favorites=True).first()
            if favstable:
                favorited = CollectionData.query.filter_by(art_id=art_id,collection_id=favstable.id).first()

        filesize = 0
        resolution = (0,0)
        imgfile = path.join(app.root_path, 'static', 'uploads', art_view.image)
        if path.isfile(imgfile):
            filesize = naturalsize(path.getsize(imgfile))
            resolution = Image.open(imgfile).size

        cat = Category.query.get(art_view.category)
        if cat.parent_id is not None:
            par_cat = Category.query.get(cat.parent_id)

            return render_template('art.haml', art=art_view, by=by,
                                   published=published, filesize=filesize,
                                   description=description,
                                   resolution=resolution,
                                   user=current_user,
                                   viewcount=viewcount,
                                   favorited=favorited,
                                   favorites_count=favorites_count,
                                   collection_count=collection_count,
                                   cat=(par_cat, cat)
                                   )

        return render_template('art.haml', art=art_view, by=by,
                               published=published,
                               filesize=filesize, description=description,
                               user=current_user,
                               resolution=resolution,
                               viewcount=viewcount,
                               favorited=favorited,
                               favorites_count=favorites_count,
                               collection_count=collection_count,
                               cat=(cat)
                               )
    return render_template('art.haml')
