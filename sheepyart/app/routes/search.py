# Base
from flask import Blueprint
from flask import render_template, request

from sheepyart.app.models import Art
from sheepyart.app.common import make_gallery

from sheepyart.sheepyart import search as search_object

search = Blueprint('search', __name__)

@search.route('/search', methods=['GET'])
def do_search():
    query = request.args.get('q', '')
    category = request.args.get('cat', 'all')

    # XXX: search: do other types as well
    try:
        results = Art.query.msearch(query)
    except:
        search_object.create_index(Art)
        results = Art.query.msearch(query)
    list = make_gallery(results, sort_new=True)
    return render_template("search.haml", list=list)
