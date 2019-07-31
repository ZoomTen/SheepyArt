# Base
from flask import Blueprint
from flask import render_template, request

search = Blueprint('search', __name__)

# FIXME: search: make this functional
@search.route('/search', methods=['GET'])
def do_search():
    query = request.args.get('q', '')
    category = request.args.get('cat', 'all')

    if query == '':
        print("no search query found!")
    else:
        print('your query:', query)
        print('of:', category)

    return render_template("search.haml", query=query)
