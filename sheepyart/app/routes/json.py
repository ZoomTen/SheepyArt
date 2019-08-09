# Base
from flask import Blueprint, Response, jsonify
from json.encoder import JSONEncoder
from sheepyart.app.common import make_category_gallery, parse_markdown

json = Blueprint('json', __name__)


def make_jsonapi(dict):
    """Makes a JSONAPI Response as defined by JSON-API 1.0.

    Args:
        dict(Dict): Any dictionary.

    Returns:
        Response with the appropriate headers.
    """
    enc = JSONEncoder()
    resp = Response(status=200)
    resp.content_type = 'application/vnd.api+json'
    # FIXME: WIP: json: Implement this JSONAPI stuff
    return resp


@json.route('/json/<user>/data', methods=['POST'])
def dump_user_data(user):
    return Response(user, status=200)


# FIXME: json: Make a separate API that complies with JSONAPI
# @json.route('/jsonapi/<user>/data', methods=['POST'])
# def dump_user_data(user):
    # converted = parse_markdown(request.form.get('content'))
    # return converted
