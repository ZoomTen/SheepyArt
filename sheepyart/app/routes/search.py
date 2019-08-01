# Base
from flask import Blueprint
from flask import render_template, request

search = Blueprint('search', __name__)

# XXX: search: make this functional
@search.route('/search', methods=['GET'])
def do_search():
    query = request.args.get('q', '')
    category = request.args.get('cat', 'all')

    return render_template("search.haml")
