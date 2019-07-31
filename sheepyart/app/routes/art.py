# Base
from flask import Blueprint
from flask import render_template, request, escape

# Database entries
from sheepyart.app.models import Art

art = Blueprint('art', __name__)

# FIXME: art: make this functional
@art.route('/art/<art_id>', methods=['GET'])
def view_art(art_id):
    art = Art.query.filter_by(id=int(art_id)).first()
    if art:
        return escape(art_id)
    else:
        return 'Art not found'
