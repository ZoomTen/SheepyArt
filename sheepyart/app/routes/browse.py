# Base
from flask import Blueprint, render_template, request
from sheepyart.app.common import make_category_gallery

browse = Blueprint('browse', __name__)


@browse.route('/', methods=['GET'])
def do_browse():
    gallery = make_category_gallery(category=None, num_entries=10,
                                    sort_new=True)

    return render_template("browse.haml",
                           gallery_snips=gallery
                           )
