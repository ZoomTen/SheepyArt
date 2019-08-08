# Base
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_required, current_user

from sheepyart.sheepyart import db
from sheepyart.app.models import Art

delete = Blueprint('delete', __name__)


@delete.route('/delete', methods=['POST'])
@login_required
def delete_art():
    # Check if the owner of the art is the same
    art = None
    art_target = request.form.get('art')
    if art_target:
        art = Art.query.get(art_target)

    if art:
        if (art.by == current_user):
            try:
                db.session.delete(art)
                db.session.commit()
            except:
                abort(500)
            return redirect(url_for('userpage.view_userpage',
                                    username=current_user.username))
    abort(403)
