"""SheepyArt collection management. Also handles favorites."""

# Base
from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for, abort, Response
from flask_login import login_required, current_user

from sheepyart.sheepyart import db
from sheepyart.app.models import Art, CollectionData, CollectionMeta

collection = Blueprint('collection', __name__)


def add_to_collection(collection, art, add_collection_name=True):
    """Add to collection

    Parameters:
        collection(CollectionMeta)
        art(Art)
        add_collection_name(Bool)
    """
    if collection:
        collection_owner_id = collection.user_id
        exists = CollectionData.query.filter_by(art_id=art.id, collection_id=collection.id).count()
        if exists > 0:
            return Response(f'Art already exists!', 500)
        else:
            if art:
                if (current_user.id == collection_owner_id):
                    collection_entry = CollectionData(art_id=art.id,
                                                      collection_id=collection.id)
                    try:
                        db.session.add(collection_entry)
                        db.session.commit()
                    except:
                        Response('There was an error with collection entry', 500)
                    # FIXME: collections: make better responses
                    if add_collection_name:
                        return Response(f"{art.title} successfully added to {collection.title}", 200)
                    else:
                        return Response(f'Successfully added to favorites!', 200)
                return Response("You don't own this collection", 403)
            return Response('No art specified!', 403)
    return Response('No collection specified!', 403)


@collection.route('/add_collection', methods=['POST'])
@login_required
def user_add_collection():
    collection = None
    art = None
    collection_id = request.form.get('collection')
    if collection_id:
        collection = CollectionMeta.query.get(collection_id)
    art_id = request.form.get('art')
    if art_id:
        art = Art.query.get(art_id)

    return add_to_collection(collection, art)


@collection.route('/add_favorite', methods=['POST'])
@login_required
def user_add_favorite():
    # NOTE: collections: User can only have one favorites table.
    # Get user's favorites table
    collection = CollectionMeta.query.filter_by(use_as_favorites=1, user_id=current_user.id).first()
    art = None
    art_id = request.form.get('art')
    if art_id:
        art = Art.query.get(art_id)

    return add_to_collection(collection, art, add_collection_name=False)


# FIXME: collections: implement collection removing.
