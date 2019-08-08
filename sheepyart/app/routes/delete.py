# Base
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_required, current_user
from flask import Response

from sheepyart.sheepyart import db
from sheepyart.app.models import Art

from os import path, remove
delete = Blueprint('delete', __name__)


@delete.route('/art/<art_id>', methods=['DELETE'])
@login_required
def delete_art(art_id):
    # Check if the owner of the art is the same
    if art_id:
        art = Art.query.get(art_id)

    if art:
        if (art.by == current_user):
            # FIXME: delete: a safer way to find static abs. path
            image_file = path.join(path.realpath('.'), 'sheepyart', 'static', 'uploads', art.image)
            thumb_file = path.join(path.realpath('.'), 'sheepyart', 'static', 'thumbnail', art.thumbnail)
            try:
                db.session.delete(art)
                db.session.commit()
            except:
                abort(500)
            try:
                remove(image_file)
                remove(thumb_file)
            except:
                return Response('Delete succeeded; however the files are still on our servers. Contact us for deletion!', 200)
            return Response('Delete succeeded.', 200)
    abort(403)
