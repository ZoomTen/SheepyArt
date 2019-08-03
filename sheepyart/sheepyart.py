'''
    SheepyArt global object
'''

from os import path

# Base app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Login support
from flask_login import LoginManager

# Haml + Sass support
from werkzeug import ImmutableDict
from flask_scss import Scss

# For the definition file
import json

# Sanitizer
from flask_bleach import Bleach

# ------------------------- Definitions -------------------------
with open(path.join("sheepyart", "app", "definitions.json"), "r") as def_files:
    # Load our JSON definition file as a dictionary that
    # we can use
    conf = json.load(def_files)

db_file = conf["db_file"]


# ------------------------- Control -------------------------


class Hamlisk(Flask):
    "Flask, but with HAMLish"
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
# app.config['SQLALCHEMY_ECHO'] = True

# Make db
db = SQLAlchemy(app)

# Compile SCSS
Scss(app)

# Login manager
logins = LoginManager(app)
logins.login_view = 'login.do_login'
logins.login_message_category = 'info'

# Sanitizer settings
app.config['BLEACH_ALLOWED_TAGS'] = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                                    'code', 'em', 'i', 'li', 'ol', 'strong',
                                    'ul', 'p', 'h1', 'h2', 'h3', 'h4', 'h5',
                                    'h6', 'pre', 'small', 'table', 'thead',
                                    'tbody', 'tfoot', 'th', 'td', 'tr'
                                     ]
app.config['BLEACH_STRIP_MARKUP'] = True

# Default sanitizer. Should there be a need for
# custom sanitizers, routes should import their
# own bleach modules
# Clorox
scrub = Bleach(app)
