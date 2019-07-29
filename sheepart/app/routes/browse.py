from flask import Blueprint
from flask import Response, render_template

browse = Blueprint('browse', __name__)


@browse.route('/', methods=['GET'])
def do_browse():
    return render_template("browse.haml")
