# Base
from flask import Blueprint, render_template, request
from sheepyart.app.common import make_category_gallery, parse_markdown

preview = Blueprint('preview', __name__)


@preview.route('/preview', methods=['POST'])
def make_preview():
    converted = parse_markdown(request.form.get('content'))
    return converted
