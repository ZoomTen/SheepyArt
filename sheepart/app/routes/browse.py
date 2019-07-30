# Base
from flask import Blueprint, render_template

browse = Blueprint('browse', __name__)


@browse.route('/', methods=['GET'])
def do_browse():
    return render_template("browse.haml")
