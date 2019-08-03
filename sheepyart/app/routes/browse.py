# Base
from flask import Blueprint, render_template, request
from sheepyart.app.common import make_category_gallery
from sheepyart.app.models import Category

browse = Blueprint('browse', __name__)


@browse.route('/', methods=['GET'])
def do_browse():
    catnum = request.args.get('cat', 0, type=int)
    category = Category.query.get(catnum)

    categories = Category.query.filter_by(parent_id=None).all()

    for i in range(len(categories)):
        id = categories[i].id
        parent = 0
        if category is not None:
            parent = category.parent_id
        check = (id == catnum) or (id == parent)
        selected = "selected" if check else None
        categories[i] = (categories[i], selected)

    if catnum <= 0:
        gallery = make_category_gallery(category=None, num_entries=10,
                                        sort_new=True)
    else:
        gallery = make_category_gallery(category=category, num_entries=10,
                                            sort_new=True)

    return render_template("browse.haml",
                           gallery_snips=gallery,
                           categories=categories,
                           catnum=catnum
                           )
