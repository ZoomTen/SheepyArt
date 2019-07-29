from os import path
from flask import Flask

# database
from flask_sqlalchemy import SQLAlchemy

# haml support
from werkzeug import ImmutableDict

# scss support
from flask_scss import Scss

# to parse definitions
import json

# App definitions and routes
from sheepart.app.routes.browse import browse
from sheepart.app.routes.search import search



# ------------------------- Definitions -------------------------

with open(path.join(__name__, "app", "definitions.json"),"r") as def_files:
    conf = json.load(def_files)

db_file = conf["db_file"]

# ------------------------- Control -------------------------
class Hamlisk(Flask):
    "Flask, but with HAML"
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape',
                    'jinja2.ext.with_',
                    'hamlish_jinja.HamlishExtension']
    )

    def __init__(self):
        Flask.__init__(self, __name__)

app = Hamlisk()

# HAMLish settings
app.jinja_env.hamlish_mode = 'indented'
app.jinja_env.hamlish_enable_div_shortcut = True

# App stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
app.config['SECRET_KEY'] = conf["secret"]

# Make db
db = SQLAlchemy(app)

# Compile SCSS
Scss(app)

# ------------------------- Models -------------------------

from sheepart.app.models import User, Art

# ------------------------- View: register endpoints -------------------------

# Register all search categories
@app.context_processor
def quack_all():
    return dict(
        search_categories=conf["search_categories"],
        site_name=conf["site_name"],
        tagline=conf["tagline"],
    )

# Register all routes
app.register_blueprint(browse)
app.register_blueprint(search)
